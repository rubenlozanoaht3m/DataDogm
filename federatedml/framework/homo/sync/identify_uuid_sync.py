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

import uuid

from federatedml.framework.homo import Scatter
from federatedml.util import consts


class Arbiter(object):

    # noinspection PyAttributeOutsideInit
    def _register_identify_uuid(self, guest_uuid_trv, host_uuid_trv, conflict_flag_trv):
        self._conflict_flag_trv = conflict_flag_trv
        self._scatter = Scatter(host_uuid_trv, guest_uuid_trv)

    def validate_uuid(self):
        ind = 0
        while True:
            uuid_set = set()
            for uid in self._scatter.get(suffix=ind):
                if uid in uuid_set:
                    self._conflict_flag_trv.remote(obj=False, role=None, idx=-1, suffix=ind)
                    ind += 1
                    break
                uuid_set.add(uid)
            else:
                break


class Client(object):

    # noinspection PyAttributeOutsideInit
    def _register_identify_uuid(self, uuid_transfer_variable, conflict_flag_transfer_variable):
        self._conflict_flag_transfer_variable = conflict_flag_transfer_variable
        self._uuid_transfer_variable = uuid_transfer_variable

    def generate_uuid(self):
        ind = -1
        while True:
            ind = ind + 1
            _uid = uuid.uuid1()
            self._uuid_transfer_variable.remote(obj=_uid, role=consts.ARBITER, idx=0, suffix=ind)
            if self._conflict_flag_transfer_variable.get(idx=0, suffix=ind):
                break
        return _uid


Host = Client
Guest = Client
