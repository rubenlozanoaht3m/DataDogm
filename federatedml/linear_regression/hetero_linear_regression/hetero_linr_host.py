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

from arch.api.utils import log_utils
from federatedml.framework.hetero.procedure import convergence
from federatedml.framework.hetero.procedure import paillier_cipher, batch_generator
from federatedml.linear_regression.hetero_linear_regression.hetero_linr_base import HeteroLinRBase
from federatedml.optim.gradient import hetero_linr_gradient_and_loss
from federatedml.secureprotol import EncryptModeCalculator
from federatedml.util import consts

LOGGER = log_utils.getLogger()


class HeteroLinRHost(HeteroLinRBase):
    def __init__(self):
        super(HeteroLinRHost, self).__init__()
        self.batch_num = None
        self.batch_index_list = []
        self.role = consts.HOST

        self.cipher = paillier_cipher.Host()
        self.batch_generator = batch_generator.Host()
        self.gradient_loss_operator = hetero_linr_gradient_and_loss.Host()
        self.converge_procedure = convergence.Host()
        self.encrypted_calculator = None

    def compute_forward(self, data_instances, coef_, intercept_, batch_index=-1):
        """
        Compute W * X + b and (W * X + b)^2, where X is the input data, W is the coefficient of lr,
        and b is the interception
        Parameters
        ----------
        data_instances: DTable of Instance, input data
        coef_: list, coefficient of lr
        intercept_: float, the interception of lr
        """
        wx = self.compute_wx(data_instances, coef_, intercept_)
        en_wx = self.encrypted_calculator[batch_index].encrypt(wx)

        return en_wx

    def fit(self, data_instances):
        """
        Train linear regression model of role host
        Parameters
        ----------
        data_instances: DTable of Instance, input data
        """

        LOGGER.info("Enter hetero_lr host")
        self._abnormal_detection(data_instances)

        self.header = self.get_header(data_instances)
        self.cipher_operator = self.cipher.gen_paillier_cipher_operator()

        self.batch_generator.initialize_batch_generator(data_instances)

        self.encrypted_calculator = [EncryptModeCalculator(self.cipher_operator,
                                                           self.encrypted_mode_calculator_param.mode,
                                                           self.encrypted_mode_calculator_param.re_encrypted_rate) for _
                                     in range(self.batch_generator.batch_nums)]

        LOGGER.info("Start initialize model.")
        model_shape = self.get_features_shape(data_instances)
        if self.init_param_obj.fit_intercept:
            self.init_param_obj.fit_intercept = False
        self.model_weights = self.initializer.init_model(model_shape, init_params=self.init_param_obj)

        while self.n_iter_ < self.max_iter:
            LOGGER.info("iter:" + str(self.n_iter_))

            batch_data_generator = self.batch_generator.generate_batch_data()
            batch_index = 0
            for batch_data in batch_data_generator:
                batch_feat_inst = self.transform(batch_data)
                optim_host_gradient = self.gradient_loss_operator.compute_gradient_procedure(
                    batch_feat_inst,
                    self.model_weights,
                    self.encrypted_calculator,
                    self.optimizer,
                    self.n_iter_,
                    batch_index)

                self.gradient_loss_operator.compute_loss(self.model_weights, self.optimizer, self.n_iter_, batch_index)

                self.model_weights = self.optimizer.update_model(self.model_weights, optim_host_gradient)
                batch_index += 1

            self.is_converged = self.converge_procedure.sync_converge_info(suffix=(self.n_iter_,))

            LOGGER.info("Get is_converged flag from arbiter:{}".format(self.is_converged))

            self.n_iter_ += 1
            LOGGER.info("iter: {}, is_converged: {}".format(self.n_iter_, self.is_converged))
            if self.is_converged:
                break

        LOGGER.info("Reach max iter {}, train model finish!".format(self.max_iter))

    def predict(self, data_instances):
        """
        Prediction of lr
        Parameters
        ----------
        data_instances:DTable of Instance, input data
        """
        LOGGER.info("Start predict ...")

        data_features = self.transform(data_instances)

        pred_host = self.compute_wx(data_features, self.model_weights.coef_, self.model_weights.intercept_)
        self.transfer_variable.host_partial_prediction.remote(pred_host, role=consts.GUEST, idx=0)
        LOGGER.info("Remote partial prediction to Guest")
