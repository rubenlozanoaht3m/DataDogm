#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  Copylast 2019 The FATE Authors. All Rights Reserved.
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


class UnionParam(BaseParam):
    """
    Define the union method for combining multiple dTables and keep entries with the same id

    Parameters
    ----------
    union_func: str, func name for union when the same id exists in provided tables, default 'first'
        'first' keeps features from first data set, 'last' keeps those from the last data set, 'all' combines features from all tables
        Note that union_func is also used to set schema for the final combined table

    need_run: bool, default True
        Indicate if this module needed to be run

    allow_missing: bool, default False
        Whether allow empty instances in the result. Note that empty tables will always be skipped regardless of this param setting.


    """

    def __init__(self, union_func='first', need_run=True, allow_missing=False):
        super().__init__()
        self.union_func = union_func
        self.need_run = need_run
        self.allow_missing = allow_missing


    def check(self):
        descr = "union param's "

        if type(self.union_func).__name__ != "str":
            raise ValueError(
                descr + "union_func {} not supported, should be bool".format(
                    self.union_func))
        if self.union_func not in ["first", "last", "all"]:
            raise ValueError(
                descr + "union_func {} not supported, should be 'first', 'last', or 'all'".format(
                    self.union_func
                )
            )

        if type(self.need_run).__name__ != "bool":
            raise ValueError(
                descr + "need_run {} not supported, should be bool".format(
                    self.need_run))

        if type(self.allow_missing).__name__ != "bool":
            raise ValueError(
                descr + "allow_missing {} not supported, should be bool".format(
                    self.allow_missing))

        LOGGER.info("Finish union parameter check!")
        return True
