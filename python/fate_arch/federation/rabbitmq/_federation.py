#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import io
import json
import sys
import time
import typing
from pickle import dumps as p_dumps, loads as p_loads

import pika
# noinspection PyPackageRequirements
from pyspark import SparkContext, RDD

from fate_arch.common import conf_utils, file_utils
from fate_arch.abc import FederationABC, GarbageCollectionABC
from fate_arch.common import Party
from fate_arch.common.log import getLogger
from fate_arch.computing.spark import get_storage_level, Table
from fate_arch.federation.rabbitmq._mq_channel import MQChannel
from fate_arch.federation.rabbitmq._rabbit_manager import RabbitManager

LOGGER = getLogger()
# default message max size in bytes = 128MB
DEFAULT_MESSAGE_MAX_SIZE = 134217728

# Datastream is a wraper of StringIO, it receives kv pairs and dump it to json string
class Datastream(object):
    def __init__(self):
        self._string = io.StringIO()
        self._string.write('[')

    def get_size(self):
        return sys.getsizeof(self._string.getvalue())

    def get_data(self):
        self._string.write(']')
        return self._string.getvalue()

    def append(self, kv: dict):
        # add ',' if not the first element
        if self._string.getvalue() != '[':
            self._string.write(',')
        json.dump(kv, self._string)

    def clear(self):
        self._string.close()
        self.__init__()

class MQ(object):
    def __init__(self, host, port, union_name, policy_id, route_table):
        self.host = host
        self.port = port
        self.union_name = union_name
        self.policy_id = policy_id
        self.route_table = route_table

    def __str__(self):
        return f"MQ(host={self.host}, port={self.port}, union_name={self.union_name}, " \
               f"policy_id={self.policy_id}, route_table={self.route_table})"

    def __repr__(self):
        return self.__str__()


class _QueueNames(object):
    def __init__(self, vhost, send, receive):
        self.vhost = vhost
        # self.union = union
        self.send = send
        self.receive = receive


class Federation(FederationABC):

    @staticmethod
    def from_conf(federation_session_id: str,
                  party: Party,
                  runtime_conf: dict,
                  rabbitmq_config: dict):

        LOGGER.debug(f"rabbitmq_config: {rabbitmq_config}")
        host = rabbitmq_config.get("host")
        port = rabbitmq_config.get("port")
        mng_port = rabbitmq_config.get("mng_port")
        base_user = rabbitmq_config.get('user')
        base_password = rabbitmq_config.get('password')

        federation_info = runtime_conf.get("job_parameters", {}).get("federation_info", {})
        union_name = federation_info.get('union_name')
        policy_id = federation_info.get("policy_id")

        rabbitmq_run = runtime_conf.get('job_parameters', {}).get('rabbitmq_run', {})
        max_message_size = rabbitmq_run.get('max_message_size', DEFAULT_MESSAGE_MAX_SIZE)
        LOGGER.debug(f'set max message size to {max_message_size} Bytes')

        rabbit_manager = RabbitManager(base_user, base_password, f"{host}:{mng_port}", rabbitmq_run)
        rabbit_manager.create_user(union_name, policy_id)
        route_table_path = rabbitmq_config.get("route_table")
        if route_table_path is None:
            route_table_path = "conf/rabbitmq_route_table.yaml"
        route_table = file_utils.load_yaml_conf(conf_path=route_table_path)
        mq = MQ(host, port, union_name, policy_id, route_table)
        return Federation(federation_session_id, party, mq, rabbit_manager, max_message_size)

    def __init__(self, session_id, party: Party, mq: MQ, rabbit_manager: RabbitManager, max_message_size):
        self._session_id = session_id
        self._party = party
        self._mq = mq
        self._rabbit_manager = rabbit_manager

        self._queue_map: typing.MutableMapping[Party, _QueueNames] = {}
        self._channels_map = {}
        self._max_message_size = max_message_size

    def get(self, name: str, tag: str, parties: typing.List[Party], gc: GarbageCollectionABC) -> typing.List:
        log_str = f"rabbitmq.get(name={name}, tag={tag}, parties={parties})"
        LOGGER.debug(f"[{log_str}]start to get")

        mq_names = self._get_mq_names(parties, name)
        LOGGER.debug(f"[rabbitmq.get]mq_names: {mq_names}")
        channel_infos = self._get_channels(mq_names=mq_names)
        LOGGER.debug(f"[rabbitmq.get]got channel infos: {channel_infos}")

        rtn = []
        for i, info in enumerate(channel_infos):
            obj = _receive(info, name, tag)  
            
            if isinstance(obj, RDD):
                rtn.append(Table(obj))
                LOGGER.debug(f"[{log_str}]received rdd({i + 1}/{len(parties)}), party: {parties[i]} ")
            else:
                rtn.append(obj)
                LOGGER.debug(f"[{log_str}]received obj({i + 1}/{len(parties)}), party: {parties[i]} ")
            
            cache_key = _get_message_cache_key(name, tag, info._party_id, info._role)
            if cache_key in message_cache:
                del message_cache[cache_key]

        LOGGER.debug(f"[{log_str}]finish to get")
        return rtn

    def remote(self, v, name: str, tag: str, parties: typing.List[Party],
               gc: GarbageCollectionABC) -> typing.NoReturn:
        log_str = f"rabbitmq.remote(name={name}, tag={tag}, parties={parties})"
        mq_names = self._get_mq_names(parties, name)
        LOGGER.debug(f"[rabbitmq.remote]mq_names: {mq_names}")

        if isinstance(v, Table):
            total_size = v.count()
            partitions = v.partitions
            LOGGER.debug(f"[{log_str}]start to remote RDD, total_size={total_size}, partitions={partitions}")

            send_func = _get_partition_send_func(name, tag, total_size, partitions, mq_names, mq=self._mq, maximun_message_size=self._max_message_size, connection_conf=self._rabbit_manager.runtime_config.get('connection', {}))
            # noinspection PyProtectedMember
            v._rdd.mapPartitions(send_func).count()
        else:
            LOGGER.debug(f"[{log_str}]start to remote obj")
            channel_infos = self._get_channels(mq_names=mq_names)
            LOGGER.debug(f"[rabbitmq.remote]got channel_infos: {channel_infos}")
            _send_obj(name=name, tag=tag, data=p_dumps(v), channel_infos=channel_infos)
        LOGGER.debug(f"[{log_str}]finish to remote")

    def cleanup(self):
        LOGGER.debug("[rabbitmq.cleanup]start to cleanup...")
        for party_id, names in self._queue_map.items():
            LOGGER.debug(f"[rabbitmq.cleanup]cleanup party_id={party_id}, names={names}.")
            self._rabbit_manager.de_federate_queue(vhost=names.vhost, receive_queue_name=names.receive)
            self._rabbit_manager.delete_queue(vhost=names.vhost, queue_name=names.send)
            self._rabbit_manager.delete_queue(vhost=names.vhost, queue_name=names.receive)
            self._rabbit_manager.delete_vhost(vhost=names.vhost)
        self._queue_map.clear()
        if self._mq.union_name:
            LOGGER.debug(f"[rabbitmq.cleanup]clean user {self._mq.union_name}.")
            self._rabbit_manager.delete_user(user=self._mq.union_name)

    def _get_mq_names(self, parties: typing.List[Party], name: str):
        mq_names = {"^".join([name, party.role, party.party_id]): self._get_or_create_queue(party, name) for party in parties}
        return mq_names

    def _get_or_create_queue(self, party: Party, name) -> _QueueNames:        
        name_party = "^".join([name, party.role, party.party_id])
        
        if name_party not in self._queue_map:
            LOGGER.debug(f"[rabbitmq.get_or_create_queue]queue for party:{party} not found, start to create")
            # gen names
            low, high = (self._party, party) if self._party < party else (party, self._party)
            # union_name = f"{low.role}-{low.party_id}-{high.role}-{high.party_id}"
            vhost_name = f"{self._session_id}-{low.role}-{low.party_id}-{high.role}-{high.party_id}"

            send_queue_name = f"send-{self._party.role}-{self._party.party_id}-{party.role}-{party.party_id}-{name}"
            receive_queue_name = f"receive-{party.role}-{party.party_id}-{self._party.role}-{self._party.party_id}-{name}"
            names = _QueueNames(vhost_name, send_queue_name, receive_queue_name)

            # initial vhost
            self._rabbit_manager.create_vhost(names.vhost)
            self._rabbit_manager.add_user_to_vhost(self._mq.union_name, names.vhost)

            # initial send queue, the name is send-${vhost}
            self._rabbit_manager.create_queue(names.vhost, names.send)

            # initial receive queue, the name is receive-${vhost}
            self._rabbit_manager.create_queue(names.vhost, names.receive)

            upstream_uri = self._upstream_uri(party_id=party.party_id)
            self._rabbit_manager.federate_queue(upstream_host=upstream_uri, vhost=names.vhost,
                                                send_queue_name=names.send, receive_queue_name=names.receive)

            self._queue_map[name_party] = names
            # TODO: check federated queue status
            LOGGER.debug(f"[rabbitmq.get_or_create_queue]queue for name: {name}, party:{party} created, names: {names}")

        names = self._queue_map[name_party]
        LOGGER.debug(f"[rabbitmq.get_or_create_queue]get queue: names: {names}")
        return names

    def _upstream_uri(self, party_id):
        host = self._mq.route_table.get(int(party_id)).get("host")
        port = self._mq.route_table.get(int(party_id)).get("port")
        upstream_uri = f"amqp://{self._mq.union_name}:{self._mq.policy_id}@{host}:{port}"
        return upstream_uri

    def _get_channels(self, mq_names):
        channel_infos = []
        for name_party, names in mq_names.items():
            name, role, party_id = name_party.split("^")
            info = self._channels_map.get(name_party)
            if info is None:
                info = _get_channel(self._mq, names, party_id=party_id, role=role, connection_conf=self._rabbit_manager.runtime_config.get('connection', {}))
                self._channels_map[name_party] = info
            channel_infos.append(info)
        return channel_infos


def _get_channel(mq, names: _QueueNames, party_id, role, connection_conf: dict):
    return MQChannel(host=mq.host, port=mq.port, user=mq.union_name, password=mq.policy_id,
                     vhost=names.vhost, send_queue_name=names.send, receive_queue_name=names.receive, 
                     party_id=party_id, role=role, extra_args=connection_conf)

def _send_kv(name, tag, data, channel_infos, total_size, partitions):
    headers = {"total_size": total_size, "partitions": partitions}
    for info in channel_infos:
        properties = pika.BasicProperties(
            content_type='application/json',
            app_id=info.party_id,
            message_id=name,
            correlation_id=tag,
            headers=headers
        )
        LOGGER.debug(f"[rabbitmq._send_kv]info: {info}, properties: {properties}.")
        info.basic_publish(body=data, properties=properties)


def _send_obj(name, tag, data, channel_infos):
    for info in channel_infos:
        properties = pika.BasicProperties(
            content_type='text/plain',
            app_id=info.party_id,
            message_id=name,
            correlation_id=tag
        )
        LOGGER.debug(f"[rabbitmq._send_obj]properties:{properties}.")
        info.basic_publish(body=data, properties=properties)


MESSAGE_MAX_SIZE = 50000

# can't pickle _thread.lock objects
def _get_channels(mq_names, mq, connection_conf: dict):
    channel_infos = []
    for name_party, names in mq_names.items():
        name, role, party_id = name_party.split("^")
        info = _get_channel(mq, names, party_id=party_id, role=role, connection_conf=connection_conf)
        channel_infos.append(info)
    return channel_infos

def _partition_snd(kvs, name, tag, total_size, partitions, mq_names, mq, maximun_message_size, connection_conf: dict):
    LOGGER.debug(
        f"[rabbitmq._partition_send]total_size:{total_size}, partitions:{partitions}, mq_names:{mq_names}, mq:{mq}.")
    channel_infos = _get_channels(mq_names=mq_names, mq=mq, connection_conf=connection_conf)

    datastream = Datastream()
    for k, v in kvs:
        el = {'k': p_dumps(k).hex(), 'v': p_dumps(v).hex()}
        # roughly caculate the size of package to avoid serialization ;)
        if datastream.get_size() + sys.getsizeof(el['k']) + sys.getsizeof(el['v']) >= maximun_message_size:
            LOGGER.debug(f'The size of message is: {datastream.get_size()}')
            _send_kv(name=name, tag=tag, data=datastream.get_data(), channel_infos=channel_infos,
                     total_size=total_size, partitions=partitions)
            datastream.clear()
        datastream.append(el)
    _send_kv(name=name, tag=tag, data=datastream.get_data(), channel_infos=channel_infos, total_size=total_size,
             partitions=partitions)
    
    return [1]


def _get_partition_send_func(name, tag, total_size, partitions, mq_names, mq, maximun_message_size, connection_conf: dict):
    def _fn(kvs):
        return _partition_snd(kvs, name, tag, total_size, partitions, mq_names, mq, maximun_message_size, connection_conf)

    return _fn


message_cache = {}


def _get_message_cache_key(name, tag, party_id, role):
    cache_key = "^".join([name, tag, str(party_id), role])
    return cache_key


def _receive(channel_info, name, tag):     
    partitions = -1
    party_id = channel_info._party_id 
    role = channel_info._role   
    wish_cache_key = _get_message_cache_key(name, tag, party_id, role)
    
    if wish_cache_key in message_cache:
        return message_cache[wish_cache_key]
    
    for method, properties, body in channel_info.consume():
        LOGGER.debug(f"[rabbitmq._receive] method: {method}, properties: {properties}.")
        if properties.message_id != name or properties.correlation_id != tag:
            # todo: fix this
            LOGGER.warning(f"[rabbitmq._receive]: require {name}.{tag}, got {properties.message_id}.{properties.correlation_id}")
        
        cache_key = _get_message_cache_key(properties.message_id, properties.correlation_id, party_id, role)
        # object
        if properties.content_type == 'text/plain':
            message_cache[cache_key] = p_loads(body)
            channel_info.basic_ack(delivery_tag=method.delivery_tag)                
           
        # rdd
        if properties.content_type == 'application/json':
            LOGGER.debug(f"[rabbitmq._receive] data: received data size is {sys.getsizeof(body)}")
            data = json.loads(body)
            data_iter = ((p_loads(bytes.fromhex(el['k'])), p_loads(bytes.fromhex(el['v']))) for el in data)
            sc = SparkContext.getOrCreate()
            partitions = properties.headers["partitions"]
            rdd = sc.parallelize(data_iter, partitions)
            if cache_key not in message_cache:
                message_cache[cache_key] = rdd
            else:
                message_cache[cache_key] = message_cache[cache_key].union(rdd).coalesce(partitions)        

            # trigger action

            message_cache[cache_key] = message_cache[cache_key].persist(get_storage_level())

            count = message_cache[cache_key].count()
            LOGGER.debug(f"count: {count}")
            channel_info.basic_ack(delivery_tag=method.delivery_tag)
            
        # object
        if properties.content_type == 'text/plain':
            if cache_key == wish_cache_key:
                channel_info.cancel()
                return message_cache[cache_key]       
        # rdd
        if properties.content_type == 'application/json':
            if cache_key == wish_cache_key and message_cache[cache_key].count() == properties.headers["total_size"]:
                channel_info.cancel()
                return message_cache[cache_key]
