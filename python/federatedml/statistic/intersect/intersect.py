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

import random

from federatedml.model_base import ModelBase
from federatedml.param.intersect_param import IntersectParam
from federatedml.secureprotol import gmpy_math
from federatedml.secureprotol.encrypt import RsaEncrypt
from federatedml.secureprotol.hash.hash_factory import Hash
from federatedml.util import consts
from federatedml.util import LOGGER
from federatedml.transfer_variable.transfer_class.raw_intersect_transfer_variable import RawIntersectTransferVariable
from federatedml.transfer_variable.transfer_class.rsa_intersect_transfer_variable import RsaIntersectTransferVariable


class Intersect(ModelBase):
    def __init__(self):
        super().__init__()
        self.model_param = IntersectParam()
        self.transfer_variable = None
        self._summary = {}

        self._guest_id = None
        self._host_id = None
        self._host_id_list = None

    def _init_model(self, param):
        self.only_output_key = param.only_output_key
        self.sync_intersect_ids = param.sync_intersect_ids

    @property
    def guest_party_id(self):
        return self._guest_id

    @guest_party_id.setter
    def guest_party_id(self, guest_id):
        if not isinstance(guest_id, int):
            raise ValueError("party id should be integer, but get {}".format(guest_id))
        self._guest_id = guest_id

    @property
    def host_party_id(self):
        return self._host_id

    @host_party_id.setter
    def host_party_id(self, host_id):
        if not isinstance(host_id, int):
            raise ValueError("party id should be integer, but get {}".format(host_id))
        self._host_id = host_id

    @property
    def host_party_id_list(self):
        return self._host_id_list

    @host_party_id_list.setter
    def host_party_id_list(self, host_id_list):
        if not isinstance(host_id_list, list):
            raise ValueError(
                "type host_party_id should be list, but get {} with {}".format(type(host_id_list), host_id_list))
        self._host_id_list = host_id_list

    def run(self, data_instances):
        raise NotImplementedError("method init must be define")

    def set_flowid(self, flowid=0):
        if self.transfer_variable is not None:
            self.transfer_variable.set_flowid(flowid)

    def _set_schema(self, schema):
        self.schema = schema

    def _get_schema(self):
        return self.schema

    def _get_value_from_data(self, intersect_ids, data_instances):
        if intersect_ids is not None:
            intersect_ids = intersect_ids.join(data_instances, lambda i, d: d)
            intersect_ids.schema = data_instances.schema
            LOGGER.info("get intersect data_instances!")

        return intersect_ids

    @staticmethod
    def get_common_intersection(intersect_ids_list: list):
        if len(intersect_ids_list) == 1:
            return intersect_ids_list[0]

        intersect_ids = None
        for i, value in enumerate(intersect_ids_list):
            if intersect_ids is None:
                intersect_ids = value
                continue
            intersect_ids = intersect_ids.join(value, lambda id, v: "id")

        return intersect_ids

    @staticmethod
    def hash(value, hash_operator, salt=None):
        h_value = hash_operator.compute(value, postfit_salt=salt)
        return h_value


class RsaIntersect(Intersect):
    def __init__(self):
        super().__init__()
        # self.intersect_cache_param = intersect_params.intersect_cache_param
        self.pub_e = None
        self.pub_n = None
        self.e = None
        self.d = None
        self.n = None
        self.r = None
        self.transfer_variable = RsaIntersectTransferVariable()

    def _init_model(self, param):
        self.random_bit = param.random_bit
        self.rsa_params = param.rsa_params
        self.split_calculation = self.rsa_params.split_calculation
        self.random_base_fraction = self.rsa_params.random_base_fraction
        self.first_hash_operator = Hash(self.rsa_params.hash_method, self.rsa_params.base64)
        self.final_hash_operator = Hash(self.rsa_params.final_hash_method, self.rsa_params.base64)

    @staticmethod
    def generate_r_base(random_bit, count, fraction):
        if fraction:
            if isinstance(fraction, int):
                r_count = fraction
            else:
                r_count = round(count * fraction)
            if r_count >= count:
                r_count = count
        else:
            r_count = count
        return [random.SystemRandom().getrandbits(random_bit) for i in range(r_count)]

    def generate_rsa_key(self, rsa_bit=1024):
        encrypt_operator = RsaEncrypt()
        encrypt_operator.generate_key(rsa_bit)
        return encrypt_operator.get_key_pair()

    def get_rsa_key(self):
        LOGGER.info("Generate rsa keys.")
        e, d, n = self.generate_rsa_key()
        return e, d, n

    @staticmethod
    def pubkey_id_process(hash_sid, v, random_bit, rsa_e, rsa_n, rsa_r=None):
        # return (r^e % n *hash(sid), (sid, r))
        if rsa_r:
            r = rsa_r[hash_sid % len(rsa_r)]
        else:
            r = random.SystemRandom().getrandbits(random_bit)
        processed_id = gmpy_math.powmod(r, rsa_e, rsa_n) * hash_sid % rsa_n
        return processed_id, (v[0], r)

    @staticmethod
    def prvkey_id_process(hash_sid, v, rsa_d, rsa_n, final_hash_operator, salt):
        processed_id = RsaIntersect.hash(gmpy_math.powmod(hash_sid, rsa_d, rsa_n), final_hash_operator, salt)
        return processed_id, v[0]

    def cal_prvkey_ids_process_pair(self, data_instances):
        return data_instances.map(
            lambda k, v: self.prvkey_id_process(k, v, self.d, self.n,
                                                self.final_hash_operator,
                                                self.rsa_params.salt)
        )

    @staticmethod
    def sign_id(hash_sid, rsa_d, rsa_n):
        return gmpy_math.powmod(hash_sid, rsa_d, rsa_n)

    def split_calculation_process(self, data_instances):
        raise NotImplementedError("This method should not be called here")

    def unified_calculation_process(self, data_instances):
        raise NotImplementedError("This method should not be called here")


class RawIntersect(Intersect):
    def __init__(self):
        super().__init__()
        self.role = None
        self.transfer_variable = RawIntersectTransferVariable()
        # self.task_version_id = None
        # self.tracker = None

    def _init_model(self, param):
        self.with_encode = param.with_encode
        self.encode_params = param.encode_params

    def intersect_send_id(self, data_instances):
        sid_hash_pair = None
        if self.with_encode and self.encode_params.encode_method != "none":
            if Hash.is_support(self.encode_params.encode_method):
                hash_operator = Hash(self.encode_params.encode_method, self.encode_params.base64)
                sid_hash_pair = data_instances.map(
                    lambda k, v: (hash_operator.compute(k, postfit_salt=self.encode_params.salt), k))
                data_sid = sid_hash_pair.mapValues(lambda v: 1)
            else:
                raise ValueError("Unknown encode_method, please check the configuration of encode_param")
        else:
            data_sid = data_instances.mapValues(lambda v: 1)

        LOGGER.info("Send id role is {}".format(self.role))

        if self.role == consts.GUEST:
            send_ids_federation = self.transfer_variable.send_ids_guest
            recv_role = consts.HOST
        elif self.role == consts.HOST:
            send_ids_federation = self.transfer_variable.send_ids_host
            recv_role = consts.GUEST
        else:
            raise ValueError("Unknown intersect role, please check the code")

        send_ids_federation.remote(data_sid,
                                   role=recv_role,
                                   idx=-1)

        LOGGER.info("Remote data_sid to role-join")
        intersect_ids = None
        if self.sync_intersect_ids:
            if self.role == consts.HOST:
                intersect_ids_federation = self.transfer_variable.intersect_ids_guest
            elif self.role == consts.GUEST:
                intersect_ids_federation = self.transfer_variable.intersect_ids_host
            else:
                raise ValueError("Unknown intersect role, please check the code")

            recv_intersect_ids_list = intersect_ids_federation.get(idx=-1)
            LOGGER.info("Get intersect ids from role-join!")

            ids_list_size = len(recv_intersect_ids_list)
            LOGGER.info("recv_intersect_ids_list's size is {}".format(ids_list_size))

            recv_intersect_ids = self.get_common_intersection(recv_intersect_ids_list)

            if self.role == consts.GUEST and len(self.host_party_id_list) > 1:
                LOGGER.info(
                    "raw intersect send role is guest, and has {} hosts, remote the final intersect_ids to hosts".format(
                        len(self.host_party_id_list)))
                self.transfer_variable.sync_intersect_ids_multi_hosts.remote(recv_intersect_ids,
                                                                             role=consts.HOST,
                                                                             idx=-1)

            if sid_hash_pair and recv_intersect_ids is not None:
                hash_intersect_ids_map = recv_intersect_ids.join(sid_hash_pair, lambda r, s: s)
                intersect_ids = hash_intersect_ids_map.map(lambda k, v: (v, 'intersect_id'))
            else:
                intersect_ids = recv_intersect_ids
        else:
            LOGGER.info("Not Get intersect ids from role-join!")

        if not self.only_output_key:
            intersect_ids = self._get_value_from_data(intersect_ids, data_instances)

        return intersect_ids

    def intersect_join_id(self, data_instances):
        LOGGER.info("Join id role is {}".format(self.role))

        sid_hash_pair = None
        if self.with_encode and self.encode_params.encode_method != "none":
            if Hash.is_support(self.encode_params.encode_method):
                hash_operator = Hash(self.encode_params.encode_method, self.encode_params.base64)
                sid_hash_pair = data_instances.map(
                    lambda k, v: (hash_operator.compute(k, postfit_salt=self.encode_params.salt), k))
                data_sid = sid_hash_pair.mapValues(lambda v: 1)
            else:
                raise ValueError("Unknown encode_method, please check the configure of hash_param")
        else:
            data_sid = data_instances.mapValues(lambda v: 1)

        if self.role == consts.HOST:
            send_ids_federation = self.transfer_variable.send_ids_guest
        elif self.role == consts.GUEST:
            send_ids_federation = self.transfer_variable.send_ids_host
        else:
            raise ValueError("Unknown intersect role, please check the code")

        recv_ids_list = send_ids_federation.get(idx=-1)

        ids_list_size = len(recv_ids_list)
        LOGGER.info("Get ids_list from role-send, ids_list size is {}".format(len(recv_ids_list)))

        if ids_list_size == 1:
            hash_intersect_ids = recv_ids_list[0].join(data_sid, lambda i, d: "intersect_id")
        elif ids_list_size > 1:
            hash_intersect_ids_list = []
            for ids in recv_ids_list:
                hash_intersect_ids_list.append(ids.join(data_sid, lambda i, d: "intersect_id"))
            hash_intersect_ids = self.get_common_intersection(hash_intersect_ids_list)
        else:
            hash_intersect_ids = None
        LOGGER.info("Finish intersect_ids computing")

        if self.sync_intersect_ids:
            if self.role == consts.GUEST:
                intersect_ids_federation = self.transfer_variable.intersect_ids_guest
                send_role = consts.HOST
            elif self.role == consts.HOST:
                intersect_ids_federation = self.transfer_variable.intersect_ids_host
                send_role = consts.GUEST
            else:
                raise ValueError("Unknown intersect role, please check the code")

            intersect_ids_federation.remote(hash_intersect_ids,
                                            role=send_role,
                                            idx=-1)
            LOGGER.info("Remote intersect ids to role-send")

            if self.role == consts.HOST and len(self.host_party_id_list) > 1:
                LOGGER.info(
                    "raw intersect join role is host, and has {} hosts, get the final intersect_ids from guest".format(
                        len(self.host_party_id_list)))
                hash_intersect_ids = self.transfer_variable.sync_intersect_ids_multi_hosts.get(idx=0)

        if sid_hash_pair:
            hash_intersect_ids_map = hash_intersect_ids.join(sid_hash_pair, lambda r, s: s)
            intersect_ids = hash_intersect_ids_map.map(lambda k, v: (v, 'intersect_id'))
        else:
            intersect_ids = hash_intersect_ids

        if not self.only_output_key:
            intersect_ids = self._get_value_from_data(intersect_ids, data_instances)

        """
        if self.task_version_id is not None:
            namespace = "#".join([str(self.guest_party_id), str(self.host_party_id), "mountain"])
            for k, v in enumerate(recv_ids_list):
                table_name = '_'.join([self.task_version_id, str(k)])
                self.tracker.job_tracker.save_as_table(v, table_name, namespace)
                LOGGER.info("save guest_{}'s id in name:{}, namespace:{}".format(k, table_name, namespace))
        """
        return intersect_ids
