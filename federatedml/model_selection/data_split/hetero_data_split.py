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
from fate_flow.entity.metric import Metric, MetricMeta
from federatedml.model_base import ModelBase
from federatedml.model_selection.data_split.data_split import HeteroDataSplit
from federatedml.param.data_split_param import DataSplitParam

from federatedml.util import consts

LOGGER = log_utils.getLogger()


class HeteroDataSplitHost(HeteroDataSplit):
    def __init__(self):
        super().__init__()

class HeteroDataSplitGuest(HeteroDataSplit):
    def __init__(self):
        super().__init__()
