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
from federatedml.framework.homo.procedure import paillier_cipher
from federatedml.logistic_regression.homo_logsitic_regression.homo_lr_base import HomoLRBase
from federatedml.logistic_regression.logistic_regression_weights import LogisticRegressionWeights
from federatedml.model_selection import MiniBatch
from federatedml.optim.gradient.logistic_gradient import LogisticGradient, TaylorLogisticGradient
from federatedml.protobuf.generated import lr_model_param_pb2
from federatedml.util import consts
from federatedml.util import fate_operator

LOGGER = log_utils.getLogger()


class HomoLRHost(HomoLRBase):
    def __init__(self):
        super(HomoLRHost, self).__init__()
        self.gradient_operator = None
        self.loss_history = []
        self.is_converged = False
        self.role = consts.HOST
        self.aggregator = aggregator.Host()
        self.lr_weights = None
        self.cipher = paillier_cipher.Host()

    def _init_model(self, params):
        super()._init_model(params)
        self.cipher.register_paillier_cipher(self.transfer_variable)
        if params.encrypt_param.method in [consts.PAILLIER]:
            self.use_encrypt = True
            self.gradient_operator = TaylorLogisticGradient()
            self.re_encrypt_batches = params.re_encrypt_batches
        else:
            self.use_encrypt = False
            self.gradient_operator = LogisticGradient()

    def fit(self, data_instances):
        LOGGER.debug("Start data count: {}".format(data_instances.count()))

        self._abnormal_detection(data_instances)
        self.init_schema(data_instances)

        pubkey = self.cipher.gen_paillier_pubkey(enable=self.use_encrypt, suffix=('fit',))
        if self.use_encrypt:
            self.cipher_operator.set_public_key(pubkey)

        self.lr_weights = self._init_model_variables(data_instances)
        w = self.cipher_operator.encrypt_list(self.lr_weights.unboxed)
        self.lr_weights = LogisticRegressionWeights(w, self.lr_weights.fit_intercept)

        LOGGER.debug("After init, lr_weights: {}".format(self.lr_weights.unboxed))

        mini_batch_obj = MiniBatch(data_inst=data_instances, batch_size=self.batch_size)

        total_batch_num = mini_batch_obj.batch_nums

        if self.use_encrypt:
            re_encrypt_times = total_batch_num // self.re_encrypt_batches
            LOGGER.debug("re_encrypt_times is :{}, batch_size: {}, total_batch_num: {}, re_encrypt_batches: {}".format(
                re_encrypt_times, self.batch_size, total_batch_num, self.re_encrypt_batches))
            self.cipher.set_re_cipher_time(re_encrypt_times)

        total_data_num = data_instances.count()
        LOGGER.debug("Current data count: {}".format(total_data_num))

        lr_weights = self.lr_weights
        while self.n_iter_ < self.max_iter:
            batch_data_generator = mini_batch_obj.mini_batch_data_generator()

            if self.n_iter_ > 0 and self.n_iter_ % self.aggregate_iters == 0:
                weight = self.aggregator.aggregate_then_get(lr_weights, degree=total_data_num,
                                                            suffix=self.n_iter_)
                self.lr_weights = LogisticRegressionWeights(weight.unboxed, self.fit_intercept)
                if not self.use_encrypt:
                    loss = self._compute_loss(data_instances)
                    self.aggregator.send_loss(loss, degree=total_data_num, suffix=(self.n_iter_,))
                    LOGGER.info("n_iters: {}, loss: {}".format(self.n_iter_, loss))
                self.is_converged = self.aggregator.get_converge_status(suffix=(self.n_iter_,))
                LOGGER.info("n_iters: {}, is_converge: {}".format(self.n_iter_, self.is_converged))
                if self.is_converged:
                    break
                lr_weights = self.lr_weights

            batch_num = 0
            for batch_data in batch_data_generator:
                n = batch_data.count()
                f = functools.partial(self.gradient_operator.compute_gradient,
                                      coef=lr_weights.coef_,
                                      intercept=lr_weights.intercept_,
                                      fit_intercept=self.fit_intercept)
                grad = batch_data.mapPartitions(f).reduce(fate_operator.reduce_add)
                grad /= n
                lr_weights = self.optimizer.update_model(lr_weights, grad, has_applied=False)
                batch_num += 1
                if self.use_encrypt and batch_num % self.re_encrypt_batches == 0:
                    w = self.cipher.re_cipher(w=lr_weights.unboxed,
                                              iter_num=self.n_iter_,
                                              batch_iter_num=batch_num)
                    lr_weights = LogisticRegressionWeights(w, self.fit_intercept)
            self.n_iter_ += 1

    def predict(self, data_instances):
        self._abnormal_detection(data_instances)
        self.init_schema(data_instances)
        suffix = ('predict',)
        pubkey = self.cipher.gen_paillier_pubkey(enable=self.use_encrypt, suffix=suffix)
        if self.use_encrypt:
            self.cipher_operator.set_public_key(pubkey)

        if self.use_encrypt:
            final_model = self.transfer_variable.aggregated_model.get(idx=0, suffix=suffix)
            lr_weights = LogisticRegressionWeights(final_model.unboxed, self.fit_intercept)
            wx = self.compute_wx(data_instances, lr_weights.coef_, lr_weights.intercept_)
            self.transfer_variable.predict_wx.remote(wx, consts.ARBITER, 0, suffix=suffix)
            predict_result = self.transfer_variable.predict_result.get(idx=0, suffix=suffix)
            predict_result = predict_result.join(data_instances, lambda p, d: [d.label, p, None,
                                                                                     {"0": None, "1": None}])

        else:
            predict_wx = self.compute_wx(data_instances, self.lr_weights.coef_, self.lr_weights.intercept_)
            pred_table = self.classify(predict_wx, self.model_param.predict_param.threshold)
            predict_result = data_instances.mapValues(lambda x: x.label)
            predict_result = pred_table.join(predict_result, lambda x, y: [y, x[1], x[0],
                                                                           {"1": x[0], "0": 1 - x[0]}])
        return predict_result

    def _get_param(self):
        if self.need_one_vs_rest:
            one_vs_rest_class = list(map(str, self.one_vs_rest_obj.classes))
            param_protobuf_obj = lr_model_param_pb2.LRModelParam(iters=self.n_iter_,
                                                                 loss_history=self.loss_history,
                                                                 is_converged=self.is_converged,
                                                                 weight={},
                                                                 intercept=0,
                                                                 need_one_vs_rest=self.need_one_vs_rest,
                                                                 one_vs_rest_classes=one_vs_rest_class)
            return param_protobuf_obj

        header = self.header

        weight_dict = {}
        intercept = 0
        if not self.use_encrypt:
            lr_vars = self.lr_weights.coef_
            for idx, header_name in enumerate(header):
                coef_i = lr_vars[idx]
                weight_dict[header_name] = coef_i
            intercept = self.lr_weights.intercept_

        param_protobuf_obj = lr_model_param_pb2.LRModelParam(iters=self.n_iter_,
                                                             loss_history=self.loss_history,
                                                             is_converged=self.is_converged,
                                                             weight=weight_dict,
                                                             intercept=intercept,
                                                             need_one_vs_rest=self.need_one_vs_rest,
                                                             header=header)
        from google.protobuf import json_format
        json_result = json_format.MessageToJson(param_protobuf_obj)
        LOGGER.debug("json_result: {}".format(json_result))
        return param_protobuf_obj
