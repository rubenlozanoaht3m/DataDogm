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

import numpy as np

from federatedml.framework.weights import ListVariables
from federatedml.framework.weights import TransferableVariables


class LogisticRegressionVariables(ListVariables):
    def __init__(self, l, fit_intercept):
        super().__init__(l)
        self.fit_intercept = fit_intercept

    def for_remote(self):
        return TransferableVariables(np.array(self._parameter))

    @property
    def coef_(self):
        if self.fit_intercept:
            return np.array(self._parameter[:-1])
        return np.array(self._parameter)

    @property
    def intercept_(self):
        if self.fit_intercept:
            return self._parameter[-1]
        return 0.0

    @property
    def parameters(self):
        return np.array(self._parameter)
