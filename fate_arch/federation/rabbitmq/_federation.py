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

import json
import typing
from pickle import dumps as p_dumps, loads as p_loads

import pika
# noinspection PyPackageRequirements
from pyspark import SparkContext, RDD

from fate_arch.abc import FederationABC, GarbageCollectionABC
from fate_arch.common import Party
from fate_arch.common.log import getLogger
from fate_arch.computing.spark import get_storage_level, Table
from fate_arch.federation.rabbitmq._mq_channel import MQChannel
from fate_arch.federation.rabbitmq._rabbit_manager import RabbitManager

LOGGER = getLogger()


class MQ(object):
    def __init__(self, host, port, union_name, policy_id, mq_conf):
        self.host = host
        self.port = port
        self.union_name = union_name
        self.policy_id = policy_id
        self.mq_conf = mq_conf

    def __str__(self):
        return f"MQ(host={self.host}, port={self.port}, union_name={self.union_name}, " \
               f"policy_id={self.policy_id}, mq_conf={self.mq_conf})"

    def __repr__(self):
        return self.__str__()


class _QueueNames(object):
    def __init__(self, vhost, union, send, receive):
        self.vhost = vhost
        self.union = union
        self.send = send
        self.receive = receive


class Federation(FederationABC):

    @staticmethod
    def from_conf(federation_session_id: str,
                  party: Party,
                  runtime_conf: dict,
                  service_conf: dict):

        mq_address = service_conf
        LOGGER.debug(f'mq_address: {mq_address}')
        rabbitmq_conf = mq_address.get("self")

        host = rabbitmq_conf.get("host")
        port = rabbitmq_conf.get("port")
        mng_port = rabbitmq_conf.get("mng_port")
        base_user = rabbitmq_conf.get('user')
        base_password = rabbitmq_conf.get('password')

        federation_info = runtime_conf.get("job_parameters", {}).get("federation_info", {})
        union_name = federation_info.get('union_name')
        policy_id = federation_info.get("policy_id")

        rabbit_manager = RabbitManager(base_user, base_password, f"{host}:{mng_port}")
        rabbit_manager.create_user(union_name, policy_id)
        mq = MQ(host, port, union_name, policy_id, mq_address)
        return Federation(federation_session_id, party, mq, rabbit_manager)

    def __init__(self, session_id, party: Party, mq: MQ, rabbit_manager: RabbitManager):
        self._session_id = session_id
        self._party = party
        self._mq = mq
        self._rabbit_manager = rabbit_manager

        self._queue_map: typing.MutableMapping[Party, _QueueNames] = {}
        self._channels_map = {}

    def get(self, name, tag, parties: typing.List[Party], gc: GarbageCollectionABC) -> typing.List:
        log_str = f"federation.get(name={name}, tag={tag}, parties={parties})"
        LOGGER.debug(f"[{log_str}]start to get obj")

        mq_names = self._get_mq_names(parties)
        channel_infos = self._get_channels(mq_names=mq_names)

        rtn = []
        for info in channel_infos:
            obj = _receive(info, name, tag)
            LOGGER.info(f'federation got data. name: {name}, tag: {tag}')
            if isinstance(obj, RDD):
                rtn.append(Table(obj))
            else:
                rtn.append(obj)
        LOGGER.debug("finish get obj, name={}, tag={}, parties={}.".format(name, tag, parties))
        return rtn

    def remote(self, v, name: str, tag: str, parties: typing.List[Party],
               gc: GarbageCollectionABC) -> typing.NoReturn:
        LOGGER.debug("start to remote obj, name={}, tag={}, parties={}.".format(name, tag, parties))
        mq_names = self._get_mq_names(parties)

        if isinstance(v, Table):
            total_size = v.count()
            partitions = v.partitions
            LOGGER.debug("start to remote RDD, total_size={}, partitions={}.".format(total_size, partitions))
            send_func = _get_partition_send_func(name, tag, total_size, partitions, mq_names, mq=self._mq)
            # noinspection PyProtectedMember
            v._rdd.mapPartitions(send_func).collect()
        else:
            channel_infos = self._get_channels(mq_names=mq_names)
            _send_obj(name=name, tag=tag, data=p_dumps(v), channel_infos=channel_infos)
        LOGGER.debug("finish remote obj, name={}, tag={}, parties={}.".format(name, tag, parties))

    def cleanup(self):
        LOGGER.debug("federation start to cleanup...")
        for party_id, names in self._queue_map.items():
            LOGGER.debug(f"cleanup party_id={party_id}, names={names}.")
            self._rabbit_manager.de_federate_queue(union_name=names.union, vhost=names.vhost)
            self._rabbit_manager.delete_queue(vhost=names.vhost, queue_name=names.send)
            self._rabbit_manager.delete_queue(vhost=names.vhost, queue_name=names.receive)
            self._rabbit_manager.delete_vhost(vhost=names.vhost)
        self._queue_map.clear()
        if self._mq.union_name:
            LOGGER.debug(f"clean user {self._mq.union_name}.")
            self._rabbit_manager.delete_user(user=self._mq.union_name)

    def _get_mq_names(self, parties: typing.List[Party]):
        mq_names = {party: self._get_or_create_queue(party) for party in parties}
        LOGGER.debug("get_mq_names:{}".format(mq_names))
        return mq_names

    def _get_or_create_queue(self, party: Party) -> _QueueNames:
        if party not in self._queue_map:
            # gen names
            low, high = (self._party, party) if self._party < party else (party, self._party)
            union_name = f"{low.role}-{low.party_id}-{high.role}-{high.party_id}"
            vhost_name = f"{self._session_id}-{union_name}"
            names = _QueueNames(vhost_name, union_name, f"send-{vhost_name}", f"receive-{vhost_name}")

            # initial vhost
            self._rabbit_manager.create_vhost(names.vhost)
            self._rabbit_manager.add_user_to_vhost(self._mq.union_name, names.vhost)

            # initial send queue, the name is send-${vhost}
            self._rabbit_manager.create_queue(names.vhost, names.send)

            # initial receive queue, the name is receive-${vhost}
            self._rabbit_manager.create_queue(names.vhost, names.receive)

            upstream_uri = self._upstream_uri(party_id=party.party_id)
            self._rabbit_manager.federate_queue(upstream_host=upstream_uri, vhost=names.vhost, union_name=names.union)

            self._queue_map[party] = names

        names = self._queue_map[party]
        LOGGER.debug(f"get_mq_names, party={party}, self._mq={self._mq}, names={names}")
        return names

    def _upstream_uri(self, party_id):
        host = self._mq.mq_conf.get(str(party_id)).get("host")
        port = self._mq.mq_conf.get(str(party_id)).get("port")
        upstream_uri = f"amqp://{self._mq.union_name}:{self._mq.policy_id}@{host}:{port}"
        return upstream_uri

    def _get_channels(self, mq_names: typing.MutableMapping[Party, _QueueNames]):
        LOGGER.debug("mq_names:{}.".format(mq_names))
        channel_infos = []
        for party, names in mq_names.items():
            info = self._channels_map.get(party)
            if info is None:
                info = _get_channel(self._mq, names)
                self._channels_map[party] = info
            channel_infos.append(info)
        LOGGER.debug("got channel_infos.")
        return channel_infos


def _get_channel(mq, names: _QueueNames):
    return MQChannel(host=mq.host, port=mq.port, user=mq.union_name, password=mq.policy_id,
                     vhost=names.vhost, send_queue_name=names.send, receive_queue_name=names.receive)


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
        LOGGER.debug("_send_kv, info:{}, properties:{}.".format(info, properties))
        info.basic_publish(body=json.dumps(data), properties=properties)


def _send_obj(name, tag, data, channel_infos):
    for info in channel_infos:
        properties = pika.BasicProperties(
            content_type='text/plain',
            app_id=info.party_id,
            message_id=name,
            correlation_id=tag
        )
        LOGGER.debug("_send_obj, properties:{}.".format(properties))
        info.basic_publish(body=data, properties=properties)


# can't pickle _thread.lock objects
def _get_channels(mq_names, mq):
    channel_infos = []
    for party, names in mq_names.items():
        info = _get_channel(mq, names)
        channel_infos.append(info)
    return channel_infos


MESSAGE_MAX_SIZE = 200000


def _partition_snd(kvs, name, tag, total_size, partitions, mq_names, mq):
    LOGGER.debug(
        f"_partition_send, total_size:{total_size}, partitions:{partitions}, mq_names:{mq_names}, mq:{mq}.")
    channel_infos = _get_channels(mq_names=mq_names, mq=mq)
    data = []
    lines = 0
    for k, v in kvs:
        el = {'k': p_dumps(k).hex(), 'v': p_dumps(v).hex()}
        data.append(el)
        lines = lines + 1
        if lines > MESSAGE_MAX_SIZE:
            _send_kv(name=name, tag=tag, data=data, channel_infos=channel_infos,
                     total_size=total_size, partitions=partitions)
            lines = 0
            data.clear()
    _send_kv(name=name, tag=tag, data=data, channel_infos=channel_infos, total_size=total_size,
             partitions=partitions)
    return data


def _get_partition_send_func(name, tag, total_size, partitions, mq_names, mq):
    def _fn(kvs):
        return _partition_snd(kvs, name, tag, total_size, partitions, mq_names, mq)

    return _fn


def _receive(channel_info, name, tag):
    count = 0
    obj = None
    for method, properties, body in channel_info.consume():
        LOGGER.debug("_receive, count:{}, method:{}, properties:{}.".format(count, method, properties))
        if properties.message_id == name and properties.correlation_id == tag:
            if properties.content_type == 'text/plain':
                obj = p_loads(body)
                channel_info.basic_ack(delivery_tag=method.delivery_tag)
                break
            elif properties.content_type == 'application/json':
                data = json.loads(body)
                count += len(data)
                data_iter = ((p_loads(bytes.fromhex(el['k'])), p_loads(bytes.fromhex(el['v']))) for el in data)
                sc = SparkContext.getOrCreate()
                if obj:
                    rdd = sc.parallelize(data_iter, properties.headers["partitions"])
                    obj = obj.union(rdd)
                    LOGGER.debug("before coalesce: federation get union partition %d, count: %d" % (
                        obj.getNumPartitions(), obj.count()))
                    obj = obj.coalesce(properties.headers["partitions"])
                    LOGGER.debug("end coalesce: federation get union partition %d, count: %d" % (
                        obj.getNumPartitions(), obj.count()))
                else:
                    obj = sc.parallelize(data_iter, properties.headers["partitions"]) \
                        .persist(get_storage_level())
                if count == properties.headers["total_size"]:
                    channel_info.basic_ack(delivery_tag=method.delivery_tag)
                    break

            channel_info.basic_ack(delivery_tag=method.delivery_tag)
    # return any pending messages
    channel_info.cancel()
    return obj
