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

import numpy as np

from federatedml.model_base import ModelBase
from federatedml.feature.imputer import Imputer
from federatedml.protobuf.generated.feature_imputation_meta_pb2 import FeatureImputationMeta, FeatureImputerMeta
from federatedml.protobuf.generated.feature_imputation_param_pb2 import FeatureImputationParam, FeatureImputerParam
from federatedml.statistic.data_overview import get_header
from federatedml.util import LOGGER
from federatedml.util.io_check import assert_io_num_rows_equal


class FeatureImputation(ModelBase):
    def __init__(self):
        super(FeatureImputation, self).__init__()
        self.summary_obj = None
        self.missing_impute_rate = None
        self.header = None
        self.cols_replace_method = None
        from federatedml.param.feature_imputation_param import FeatureImputationParam
        self.model_param = FeatureImputationParam()

        self.model_param_name = 'FeatureImputationParam'
        self.model_meta_name = 'FeatureImputationMeta'

    def _init_model(self, model_param):
        self.missing_fill_method = model_param.missing_fill_method
        self.col_missing_fill_method = model_param.col_missing_fill_method
        self.default_value = model_param.default_value
        self.missing_impute = model_param.missing_impute

    def get_summary(self):
        missing_summary = dict()
        missing_summary["missing_value"] = list(self.missing_impute)
        missing_summary["missing_impute_value"] = dict(zip(self.header, self.default_value))
        missing_summary["missing_impute_rate"] = dict(zip(self.header, self.missing_impute_rate))
        return missing_summary

    def load_model(self, model_dict):
        param_obj = list(model_dict.get('model').values())[0].get(self.model_param_name)
        meta_obj = list(model_dict.get('model').values())[0].get(self.model_meta_name)
        self.header = param_obj.header
        self.missing_fill, self.missing_fill_method, \
        self.missing_impute, self.default_value = load_feature_imputer_model(self.header,
                                                                             "Imputer",
                                                                             meta_obj.imputer_meta,
                                                                             param_obj.imputer_param)

    def save_model(self):
        meta_obj, param_obj = save_feature_imputer_model(missing_fill=True,
                                                         missing_replace_method=self.missing_fill_method,
                                                         missing_impute=self.missing_impute,
                                                         missing_fill_value=self.default_value,
                                                         missing_replace_rate=self.missing_impute_rate,
                                                         cols_replace_method=self.cols_replace_method,
                                                         header=self.header)


        return meta_obj, param_obj

    def export_model(self):
        missing_imputer_meta, missing_imputer_param = self.save_model()
        meta_obj = FeatureImputationMeta(need_run=self.need_run,
                                         imputer_meta=missing_imputer_meta)
        param_obj = FeatureImputationParam(header=self.header,
                                           imputer_param=missing_imputer_param)
        model_dict = {
            self.model_meta_name: meta_obj,
            self.model_param_name: param_obj
        }

        return model_dict

    @assert_io_num_rows_equal
    def fit(self, data):
        LOGGER.info(f"Enter Feature Imputation fit")
        imputer_processor = Imputer(self.missing_impute)
        imputed_data, self.default_value = imputer_processor.fit(data,
                                                                 replace_method=self.missing_fill_method,
                                                                 replace_value=self.default_value,
                                                                 col_replace_method=self.col_missing_fill_method)
        if self.missing_impute is None:
            self.missing_impute = imputer_processor.get_missing_value_list()
        self.missing_impute_rate = imputer_processor.get_impute_rate("fit")
        self.header = get_header(imputed_data)
        self.cols_replace_method = imputer_processor.cols_replace_method
        self.set_summary(self.get_summary())

        return imputed_data

    @assert_io_num_rows_equal
    def transform(self, data):
        LOGGER.info(f"Enter Feature Imputation transform")
        imputer_processor = Imputer(self.missing_impute)
        imputed_data = imputer_processor.transform(data, transform_value=self.default_value)
        if self.missing_impute is None:
            self.missing_impute = imputer_processor.get_missing_value_list()

        self.missing_impute_rate = imputer_processor.get_impute_rate("transform")
        return imputed_data


def save_feature_imputer_model(missing_fill=False,
                               missing_replace_method=None,
                               missing_impute=None,
                               missing_fill_value=None,
                               missing_replace_rate=None,
                               cols_replace_method=None,
                               header=None):
    model_meta = FeatureImputerMeta()
    model_param = FeatureImputerParam()

    model_meta.is_imputer = missing_fill
    if missing_fill:
        if missing_replace_method:
            model_meta.strategy = missing_replace_method

        if missing_impute is not None:
            model_meta.missing_value.extend(map(str, missing_impute))
            model_meta.missing_value_type.extend([type(v).__name__ for v in missing_impute])

        if missing_fill_value is not None:
            feature_value_dict = dict(zip(header,missing_fill_value))
            model_param.missing_replace_value.update(feature_value_dict)
            missing_fill_value_type = [type(v).__name__ for v in missing_fill_value]
            feature_value_type_dict = dict(zip(header, missing_fill_value_type))
            model_param.missing_replace_value_type.update(feature_value_type_dict)

        if missing_replace_rate is not None:
            missing_replace_rate_dict = dict(zip(header, missing_replace_rate))
            model_param.missing_value_ratio.update(missing_replace_rate_dict)

        if cols_replace_method is not None:
            cols_replace_method_dict = cols_replace_method
            if not isinstance(cols_replace_method, dict):
                cols_replace_method_dict = dict(zip(header, cols_replace_method))
            model_meta.cols_strategy.update(cols_replace_method_dict)

    return model_meta, model_param


def load_value_to_type(value, value_type):
    if value_type in ["int", "int64", "long", "float", "float64", "double"]:
        loaded_value = getattr(np, value_type)(value)
    elif value_type in ["str", "_str"]:
        loaded_value = str(value)
    else:
        raise ValueError(f"unknown value type: {value_type}")
    return loaded_value


def load_feature_imputer_model(header=None,
                               model_name="Imputer",
                               model_meta=None,
                               model_param=None):
    missing_fill = model_meta.is_imputer
    missing_replace_method = model_meta.strategy
    missing_value = list(model_meta.missing_value)
    missing_value_type = list(model_meta.missing_value_type)
    missing_fill_value = model_param.missing_replace_value
    missing_fill_value_type = model_param.missing_replace_value_type


    if missing_fill:
        if not missing_replace_method:
            missing_replace_method = None

        if not missing_value:
            missing_value = None
        else:
            missing_value = [load_value_to_type(missing_value[i],
                                                missing_value_type[i]) for i in range(len(missing_value))]

        if missing_fill_value:
            missing_fill_value = [load_value_to_type(missing_fill_value.get(head),
                                                     missing_fill_value_type[head]) for head in header]
        else:
            missing_fill_value = None
    else:
        missing_replace_method = None
        missing_value = None
        missing_fill_value = None

    return missing_fill, missing_replace_method, missing_value, missing_fill_value
