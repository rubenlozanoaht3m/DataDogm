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

import functools

from arch.api.utils import log_utils
from federatedml.framework.homo.procedure import aggregator, predict_procedure
from federatedml.logistic_regression.homo_logsitic_regression.homo_lr_base import HomoLRBase
from federatedml.logistic_regression.logistic_regression_variables import LogisticRegressionVariables
from federatedml.model_selection import MiniBatch
from federatedml.optim.gradient.logistic_gradient import LogisticGradient
from federatedml.statistic import data_overview
from federatedml.util import consts
from federatedml.util import fate_operator

LOGGER = log_utils.getLogger()


class HomoLRGuest(HomoLRBase):
    def __init__(self):
        super(HomoLRGuest, self).__init__()
        self.gradient_operator = LogisticGradient()
        self.loss_history = []
        self.role = consts.GUEST
        self.aggregator = aggregator.Guest()
        self.predict_procedure = predict_procedure.Guest()

    def _init_model(self, params):
        super()._init_model(params)
        self.predict_procedure.register_predict_sync(self.transfer_variable, self)

    def fit(self, data_instances):

        self._abnormal_detection(data_instances)
        self.init_schema(data_instances)

        self.lr_variables = self.__init_model(data_instances)

        max_iter = self.max_iter
        mini_batch_obj = MiniBatch(data_inst=data_instances, batch_size=self.batch_size)
        iter_loss = 0
        while self.n_iter_ < max_iter:
            batch_data_generator = mini_batch_obj.mini_batch_data_generator()

            batch_num = 0
            for batch_data in batch_data_generator:
                n = batch_data.count()
                f = functools.partial(self.gradient_operator.compute,
                                      coef=self.lr_variables.coef_,
                                      intercept=self.lr_variables.intercept_,
                                      fit_intercept=self.fit_intercept)
                grad_loss = batch_data.mapPartitions(f)
                grad, loss = grad_loss.reduce(fate_operator.reduce_add)
                LOGGER.debug('iter: {}, batch_index: {}, grad: {}, loss: {}, n: {}, iter_loss :{}'.format(
                    self.n_iter_, batch_num,
                    grad, loss, n, iter_loss))
                grad /= n
                loss /= n
                self.lr_variables = self.optimizer.update_model(self.lr_variables, grad, has_applied=False)
                loss_norm = self.optimizer.loss_norm(self.lr_variables)
                iter_loss += loss
                if loss_norm is not None:
                    iter_loss += loss_norm
                batch_num += 1
            iter_loss /= batch_num
            self.callback_loss(self.n_iter_, iter_loss)
            self.loss_history.append(iter_loss)
            self.aggregator.send_model_for_aggregate(self.lr_variables, self.n_iter_)
            self.aggregator.send_loss(iter_loss, self.n_iter_)
            weight = self.aggregator.get_aggregated_model(self.n_iter_)
            self.lr_variables = LogisticRegressionVariables(weight.parameters, self.fit_intercept)
            self.is_converged = self.aggregator.get_converge_status(suffix=(self.n_iter_,))
            LOGGER.info("n_iters: {}, converge flag is :{}".format(self.n_iter_, self.is_converged))
            if self.is_converged:
                break
            self.n_iter_ += 1

    def predict(self, data_instances):
        self._abnormal_detection(data_instances)
        self.init_schema(data_instances)
        predict_result = self.predict_procedure.start_predict(data_instances,
                                                              self.lr_variables,
                                                              self.model_param.predict_param.threshold)
        return predict_result

    def __init_model(self, data_instances):
        model_shape = data_overview.get_features_shape(data_instances)

        LOGGER.info("Initialized model shape is {}".format(model_shape))

        lr_variables = self.initializer.init_model(model_shape, init_params=self.init_param_obj)
        return lr_variables
