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
import atexit
import socket
from urllib import parse

from kazoo.client import KazooClient
from kazoo.security import make_digest_acl
from kazoo.exceptions import NodeExistsError

from fate_arch.common import conf_utils
from fate_arch.common.conf_utils import get_base_config
from fate_flow.settings import FATE_FLOW_MODEL_TRANSFER_ENDPOINT, IP, HTTP_PORT, FATEFLOW_SERVICE_NAME
from fate_flow.settings import stat_logger, SERVICES_SUPPORT_REGISTRY, FATE_SERVICES_REGISTERED_PATH


class ServiceUtils(object):
    ZOOKEEPER_CLIENT = None
    registry_service_info = {
        "fatemanager": ["host", "port", "federatedId"],
        "studio": ["host", "port"]
    }

    @classmethod
    def get(cls, service_name, default=None):
        if get_base_config("use_registry", False) and service_name in SERVICES_SUPPORT_REGISTRY:
            return ServiceUtils.get_from_registry(service_name)
        return ServiceUtils.get_from_file(service_name, default)

    @classmethod
    def get_item(cls, service_name, key, default=None):
        return ServiceUtils.get(service_name, {}).get(key, default)

    @classmethod
    def get_from_file(cls, service_name, default=None):
        return conf_utils.get_base_config(service_name, default)

    @classmethod
    def get_zk(cls, ):
        zk_config = get_base_config("zookeeper", {})
        if zk_config.get("use_acl", False):
            default_acl = make_digest_acl(zk_config.get("user", ""), zk_config.get("password", ""), all=True)
            zk = KazooClient(hosts=zk_config.get("hosts", []), default_acl=[default_acl], auth_data=[("digest", "{}:{}".format(
                zk_config.get("user", ""), zk_config.get("password", "")))])
        else:
            zk = KazooClient(hosts=zk_config.get("hosts", []))
        return zk

    @classmethod
    def get_from_registry(cls, service_name):
        try:
            zk = ServiceUtils.get_zk()
            zk.start()
            nodes = zk.get_children(FATE_SERVICES_REGISTERED_PATH.get(service_name, ""))
            services = nodes_unquote(nodes)
            zk.stop()
            return services
        except Exception as e:
            raise Exception('loading servings node  failed from zookeeper: {}'.format(e))

    @classmethod
    def register(cls, zk=None, party_model_id=None, model_version=None):
        if not get_base_config('use_registry', False):
            return
        if not zk:
            zk = ServiceUtils.get_zk()
            zk.start()
            atexit.register(zk.stop)
        model_transfer_url = 'http://{}:{}{}'.format(IP, HTTP_PORT, FATE_FLOW_MODEL_TRANSFER_ENDPOINT)
        if party_model_id is not None and model_version is not None:
            model_transfer_url += '/{}/{}'.format(party_model_id.replace('#', '~'), model_version)
        fate_flow_model_transfer_service = '{}/{}'.format(FATE_SERVICES_REGISTERED_PATH.get(FATEFLOW_SERVICE_NAME, ""), parse.quote(model_transfer_url, safe=' '))

        try:
            zk.create(fate_flow_model_transfer_service, makepath=True, ephemeral=True)
            stat_logger.info("register path {} to {}".format(fate_flow_model_transfer_service, ";".join(get_base_config("zookeeper", {}).get("hosts"))))
        except NodeExistsError:
            pass
        except Exception as e:
            stat_logger.exception(e)

    @classmethod
    def register_models(cls, models):
        if not get_base_config('use_registry', False):
            return
        zk = ServiceUtils.get_zk()
        zk.start()
        atexit.register(zk.stop)
        for model in models:
            cls.register(zk, model.f_party_model_id, model.f_model_version)

    @classmethod
    def register_service(cls, service_config):
        update_server = {}
        for service_name, service_info in service_config.items():
            if service_name not in cls.registry_service_info.keys():
                continue
            cls.parameter_verification(service_name, service_info)
            manager_conf = conf_utils.get_base_config(service_name, {})
            if not manager_conf:
                manager_conf = service_info
            else:
                manager_conf.update(service_info)
            conf_utils.update_config(service_name, manager_conf)
            update_server[service_name] = manager_conf
        return update_server

    @classmethod
    def parameter_verification(cls,service_name, service_info):
        if set(service_info.keys()) != set(cls.registry_service_info.get(service_name)):
            raise Exception(f'the registration service {service_name} configuration item is'
                            f' {cls.registry_service_info.get(service_name)}')
        if "host" in service_info and "port" in service_info:
            cls.connection_test(service_info.get("host"), service_info.get("port"))

    @classmethod
    def connection_test(cls, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        if result != 0:
            raise ConnectionRefusedError(f"connection refused: host {ip}, port {port}")


def nodes_unquote(nodes):
    urls = [parse.unquote(node) for node in nodes]
    servers = []
    for url in urls:
        try:
            servers.append(url.split('/')[2])
        except Exception as e:
            stat_logger.exception(e)
    return servers
