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
from arch.api.utils import log_utils
from federatedml.model_selection.data_split.data_split import DataSplitter

LOGGER = log_utils.getLogger()

class HomoDataSplitHost(DataSplitter):
    def __init__(self):
        super().__init__()

    def fit(self, data_inst):
        LOGGER.debug(f"Enter Hetero {self.role} Data Split fit")
        self.param_validater(data_inst)
        ids = self._get_ids(data_inst)
        y = self._get_y(data_inst)
        id_train, id_test, id_validate = self._split(ids, y)
        train_data, test_data, validate_data = self.split_data(data_inst, id_train, id_test, id_validate)
        return train_data, test_data, validate_data

class HomoDataSplitGuest(DataSplitter):
    def __init__(self):
        super().__init__()

    def fit(self, data_inst):
        LOGGER.debug(f"Enter Hetero {self.role} Data Split fit")
        self.param_validater(data_inst)
        ids = self._get_ids(data_inst)
        y = self._get_y(data_inst)
        id_train, id_test, id_validate = self._split(ids, y)
        train_data, test_data, validate_data = self.split_data(data_inst, id_train, id_test, id_validate)
        return train_data, test_data, validate_data
