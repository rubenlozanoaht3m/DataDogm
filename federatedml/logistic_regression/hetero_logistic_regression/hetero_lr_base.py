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

from federatedml.logistic_regression.base_logistic_regression import BaseLogisticRegression
from federatedml.util import consts
from federatedml.util.transfer_variable.hetero_lr_transfer_variable import HeteroLRTransferVariable


class HeteroLRBase(BaseLogisticRegression):
    def __init__(self):
        super().__init__()
        self.model_name = 'HeteroLogisticRegression'
        self.model_param_name = 'HeteroLogisticRegressionParam'
        self.model_meta_name = 'HeteroLogisticRegressionMeta'
        self.mode = consts.HETERO
        self.aggregator = None
        self.cipher = None
        self.batch_generator = None
        self.loss_computer = None
        self.gradient_procedure = None
        self.converge_procedure = None

    def _init_model(self, params):
        super(HeteroLRBase, self)._init_model(params)
        self.transfer_variable = HeteroLRTransferVariable()
        self.cipher.register_paillier_cipher(self.transfer_variable)
        self.converge_procedure.register_convergence(self.transfer_variable)
        self.batch_generator.register_batch_generator(self.transfer_variable)
        self.gradient_procedure.register_gradient_procedure(self.transfer_variable)
        self.loss_computer.register_loss_computer(self.transfer_variable)


    def update_local_model(self, fore_gradient, data_inst, coef, **training_info):
        """
        update local model that transforms features of raw input

        This 'update_local_model' function serves as a handler on updating local model that transforms features of raw
        input into more representative features. We typically adopt neural networks as the local model, which is
        typically updated/trained based on stochastic gradient descent algorithm. For concrete implementation, please
        refer to 'hetero_dnn_logistic_regression' folder.

        For this particular class (i.e., 'BaseLogisticRegression') that serves as a base class for neural-networks-based
        hetero-logistic-regression model, the 'update_local_model' function will do nothing. In other words, no updating
        performed on the local model since there is no one.

        Parameters:
        ___________
        :param fore_gradient: a table holding fore gradient
        :param data_inst: a table holding instances of raw input of guest side
        :param coef: coefficients of logistic regression model
        :param training_info: a dictionary holding training information
        """
        pass

    def transform(self, data_inst):
        """
        transform features of instances held by 'data_inst' table into more representative features

        This 'transform' function serves as a handler on transforming/extracting features from raw input 'data_inst' of
        guest. It returns a table that holds instances with transformed features. In theory, we can use any model to
        transform features. Particularly, we would adopt neural network models such as auto-encoder or CNN to perform
        the feature transformation task. For concrete implementation, please refer to 'hetero_dnn_logistic_regression'
        folder.

        For this particular class (i.e., 'BaseLogisticRegression') that serves as a base class for neural-networks-based
        hetero-logistic-regression model, the 'transform' function will do nothing but return whatever that has been
        passed to it. In other words, no feature transformation performed on the raw input of guest.

        Parameters:
        ___________
        :param data_inst: a table holding instances of raw input of guest side
        :return: a table holding instances with transformed features
        """
        return data_inst
