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
from federatedml.param.base_param import BaseParam
from federatedml.util import consts

LOGGER = log_utils.getLogger()


class ScaleParam(BaseParam):
    """
    Define the feature scale parameters.

    Parameters
    ----------
        method : str, like scale in sklearn, now it support "min_max_scale" and "standard_scale", and will support other scale method soon.
                 Default None, which will do nothing for scale

        mode: str, the mode support "normal" and "cap". for mode is "normal", the feat_upper and feat_lower is the normal value like "10" or "3.1" and for "cap", feat_upper and
              feature_lower will between 0 and 1, which means the percentile of the column. Default "normal"

        feat_upper: int or float, the upper limit in the column. If the scaled value is larger than feat_upper, it will be set to feat_upper. Default None.
        feat_lower: int or float, the lower limit in the column. If the scaled value is less than feat_lower, it will be set to feat_lower. Default None.

        scale_col_indexes: list,the idx of column in scale_column_idx will be scaled, while the idx of column is not in, it will not be scaled.
        scale_names : list of string, default: [].Specify which columns need to scaled. Each element in the list represent for a column name in header.
        with_mean: bool, used for "standard_scale". Default False.
        with_std: bool, used for "standard_scale". Default False.
            The standard scale of column x is calculated as : z = (x - u) / s, where u is the mean of the column and s is the standard deviation of the column.
            if with_mean is False, u will be 0, and if with_std is False, s will be 1.

        need_run: bool, default True
            Indicate if this module needed to be run

    """

    def __init__(self, method=None, mode="normal", scale_col_indexes=-1, scale_names=None, feat_upper=None, feat_lower=None,
                 with_mean=True, with_std=True, need_run=True):
        super().__init__()
        if scale_names is None:
            scale_names = []

        self.method = method
        self.mode = mode
        self.feat_upper = feat_upper
        self.feat_lower = feat_lower
        self.scale_col_indexes = scale_col_indexes
        self.scale_names = scale_names

        self.with_mean = with_mean
        self.with_std = with_std

        self.need_run = need_run

    def check(self):
        if self.method is not None:
            descr = "scale param's method"
            self.method = self.check_and_change_lower(self.method,
                                                      [consts.MINMAXSCALE, consts.STANDARDSCALE],
                                                      descr)

        descr = "scale param's mode"
        self.mode = self.check_and_change_lower(self.mode,
                                                [consts.NORMAL, consts.CAP],
                                                descr)

        # if type(self.feat_upper).__name__ not in ["float", "int"]:
        #     raise ValueError("scale param's feat_upper {} not supported, should be float or int".format(
        #         self.feat_upper))
        #
        # if type(self.feat_lower).__name__ not in ["float", "int"]:
        #     raise ValueError("scale param's feat_lower {} not supported, should be float or int".format(
        #         self.feat_lower))

        if self.scale_col_indexes != -1  and not isinstance(self.scale_col_indexes, list):
            raise ValueError("scale_col_indexes is should be -1 or a list")

        if not isinstance(self.scale_names, list):
            raise ValueError("scale_names is should be a list of string")
        else:
            for e in self.scale_names:
                if not isinstance(e, str):
                    raise ValueError("scale_names is should be a list of string")

        self.check_boolean(self.with_mean, "scale_param with_mean")
        self.check_boolean(self.with_std, "scale_param with_std")
        self.check_boolean(self.need_run, "scale_param need_run")

        LOGGER.debug("Finish scale parameter check!")
        return True
