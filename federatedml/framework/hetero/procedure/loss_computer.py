#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


from arch.api.utils import log_utils
from federatedml.framework.hetero.sync import loss_sync

LOGGER = log_utils.getLogger()


class Arbiter(loss_sync.Arbiter):
    def register_loss_computer(self, transfer_variable):
        self._register_loss_sync(transfer_variable.loss)


class Guest(loss_sync.Guest):
    def register_loss_computer(self, transfer_variable):
        self._register_loss_sync(transfer_variable.host_loss_regular,
                                 transfer_variable.loss)


class Host(loss_sync.Host):
    def register_loss_computer(self, transfer_variable):
        self._register_loss_sync(transfer_variable.host_loss_regular,
                                 transfer_variable.loss)
