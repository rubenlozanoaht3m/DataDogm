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
#
from arch.api.utils import log_utils
from federatedml.util import consts
from federatedml.param.base_param import BaseParam

LOGGER = log_utils.getLogger()


class EvaluateParam(BaseParam):
    """
    Define the evaluation method of binary/multiple classification and regression

    Parameters
    ----------
    eval_type: string, support 'binary' for HomoLR, HeteroLR and Secureboosting. support 'regression' for Secureboosting. 'multi' is not support these version

    pos_label: specify positive label type, can be int, float and str, this depend on the data's label, this parameter effective only for 'binary'

    need_run: bool, default True
        Indicate if this module needed to be run
    """

    def __init__(self, eval_type="binary", pos_label=1, need_run=True, metric=None):
        super().__init__()
        self.eval_type = eval_type
        LOGGER.debug('eval type is {}'.format(self.eval_type))
        self.pos_label = pos_label
        self.need_run = need_run
        self.metric = metric

        self.default_metrics = {
            consts.BINARY: consts.DEFAULT_BINARY_METRIC,
            consts.MULTY: consts.DEFAULT_MULTI_METRIC,
            consts.REGRESSION: consts.REGRESSION_METRICS
        }

        self.allowed_metrics = {
            consts.BINARY: consts.BINARY_METRICS,
            consts.MULTY: consts.MULTI_METRICS,
            consts.REGRESSION: consts.REGRESSION_METRICS
        }

    def _check_valid_metric(self, metrics_list):

        metric_list = consts.ALL_METRIC_NAME
        alias_name: dict = consts.ALIAS

        full_name_list = []
        
        LOGGER.debug('metric list is {}'.format(metrics_list))

        for metric in metrics_list:

            metric = str.lower(metric)
            if metric in metric_list:
                full_name_list.append(metric)
                continue

            valid_flag = False
            for alias, full_name in alias_name.items():
                if metric in alias:
                    full_name_list.append(full_name)
                    valid_flag = True
                    break

            if not valid_flag:
                raise ValueError('metric {} is not supported'.format(metric))

        final_list = []
        allowed_metrics = self.allowed_metrics[self.eval_type]

        for m in full_name_list:
            if m in allowed_metrics:
                final_list.append(m)
            else:
                raise ValueError('metric {} is not used for {} task'.format(m, self.eval_type))

        if consts.RECALL in final_list or consts.PRECISION in final_list:
            final_list.append(consts.RECALL)
            final_list.append(consts.PRECISION)

        ret = list(set(final_list))
        LOGGER.debug('ret is {}'.format(ret))
        return ret

    def check(self):

        descr = "evaluate param's "
        self.eval_type = self.check_and_change_lower(self.eval_type,
                                                       [consts.BINARY, consts.MULTY, consts.REGRESSION],
                                                       descr)

        if type(self.pos_label).__name__ not in ["str", "float", "int"]:
            raise ValueError(
                "evaluate param's pos_label {} not supported, should be str or float or int type".format(
                    self.pos_label))

        if type(self.need_run).__name__ != "bool":
            raise ValueError(
                "evaluate param's need_run {} not supported, should be bool".format(
                    self.need_run))

        if self.metric is None:
            self.metric = self.default_metrics[self.eval_type]
            LOGGER.debug('use default metric {} for eval type {}'.format(self.metric, self.eval_type)) 

        self.metric = self._check_valid_metric(self.metric)

        LOGGER.info("Finish evaluation parameter check!")

        return True


if __name__ == '__main__':
    param = EvaluateParam(eval_type='binary')
    param.check()
