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
import copy

from federatedml.param.base_param import BaseParam
from federatedml.param.cross_validation_param import CrossValidationParam
from federatedml.param.encrypt_param import EncryptParam
from federatedml.param.encrypted_mode_calculation_param import EncryptedModeCalculatorParam
from federatedml.param.init_model_param import InitParam
from federatedml.param.one_vs_rest_param import OneVsRestParam
from federatedml.param.predict_param import PredictParam
from federatedml.util import consts


class LogisticParam(BaseParam):
    """
    Parameters used for Logistic Regression both for Homo mode or Hetero mode.

    Parameters
    ----------
    penalty : str, 'L1' or 'L2'. default: 'L2'
        Penalty method used in LR. Please note that, when using encrypted version in HomoLR,
        'L1' is not supported.

    eps : float, default: 1e-5
        The tolerance of convergence

    alpha : float, default: 1.0
        Regularization strength coefficient.

    optimizer : str, 'sgd', 'rmsprop', 'adam', 'nesterov_momentum_sgd' or 'adagrad', default: 'sgd'
        Optimize method

    party_weight : int or float, default: 1
        Required in Homo LR. Setting the weight of model updated for this party.
        The higher weight set, the higher influence made for this party when updating model.

    batch_size : int, default: -1
        Batch size when updating model. -1 means use all data in a batch. i.e. Not to use mini-batch strategy.

    learning_rate : float, default: 0.01
        Learning rate

    max_iter : int, default: 100
        The maximum iteration for training.

    converge_func : str, 'diff', 'weight_diff' or 'abs', default: 'diff'
        Method used to judge converge or not.
            a)	diff： Use difference of loss between two iterations to judge whether converge.
            b)  weight_diff: Use difference between weights of two consecutive iterations
            c)	abs: Use the absolute value of loss to judge whether converge. i.e. if loss < eps, it is converged.

    decay: int or float, default: 1
        Decay rate for learning rate. learning rate will follow the following decay schedule.
        lr = lr0/(1+decay*t) if decay_sqrt is False. If decay_sqrt is True, lr = lr0 / sqrt(1+decay*t)
        where t is the iter number.

    """

    def __init__(self, penalty='L2',
                 eps=1e-5, alpha=1.0, optimizer='sgd', party_weight=1,
                 batch_size=-1, learning_rate=0.01, init_param=InitParam(),
                 max_iter=100, converge_func='diff',
                 predict_param=PredictParam(), cv_param=CrossValidationParam(),
                 one_vs_rest_param=OneVsRestParam(), decay=1, decay_sqrt=True
                 ):
        super(LogisticParam, self).__init__()
        self.penalty = penalty
        self.eps = eps
        self.alpha = alpha
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.init_param = copy.deepcopy(init_param)
        self.max_iter = max_iter
        self.converge_func = converge_func
        self.party_weight = party_weight
        self.predict_param = copy.deepcopy(predict_param)
        self.cv_param = copy.deepcopy(cv_param)
        self.one_vs_rest_param = copy.deepcopy(one_vs_rest_param)
        self.decay = decay
        self.decay_sqrt = decay_sqrt

    def check(self):
        descr = "logistic_param's"

        if type(self.penalty).__name__ != "str":
            raise ValueError(
                "logistic_param's penalty {} not supported, should be str type".format(self.penalty))
        else:
            self.penalty = self.penalty.upper()
            if self.penalty not in ['L1', 'L2', 'NONE']:
                raise ValueError(
                    "logistic_param's penalty not supported, penalty should be 'L1', 'L2' or 'none'")

        if type(self.eps).__name__ != "float":
            raise ValueError(
                "logistic_param's eps {} not supported, should be float type".format(self.eps))

        if type(self.alpha).__name__ not in ["float", 'int']:
            raise ValueError(
                "logistic_param's alpha {} not supported, should be float or int type".format(self.alpha))

        if type(self.optimizer).__name__ != "str":
            raise ValueError(
                "logistic_param's optimizer {} not supported, should be str type".format(self.optimizer))
        else:
            self.optimizer = self.optimizer.lower()
            if self.optimizer not in ['sgd', 'rmsprop', 'adam', 'adagrad', 'nesterov_momentum_sgd']:
                raise ValueError(
                    "logistic_param's optimizer not supported, optimizer should be"
                    " 'sgd', 'rmsprop', 'adam', 'nesterov_momentum_sgd' or 'adagrad'")

        if self.batch_size != -1:
            if type(self.batch_size).__name__ not in ["int"] \
                    or self.batch_size < consts.MIN_BATCH_SIZE:
                raise ValueError(descr + " {} not supported, should be larger than 10 or "
                                         "-1 represent for all data".format(self.batch_size))

        if type(self.learning_rate).__name__ != "float":
            raise ValueError(
                "logistic_param's learning_rate {} not supported, should be float type".format(
                    self.learning_rate))

        self.init_param.check()

        if type(self.max_iter).__name__ != "int":
            raise ValueError(
                "logistic_param's max_iter {} not supported, should be int type".format(self.max_iter))
        elif self.max_iter <= 0:
            raise ValueError(
                "logistic_param's max_iter must be greater or equal to 1")

        if type(self.converge_func).__name__ != "str":
            raise ValueError(
                "logistic_param's converge_func {} not supported, should be str type".format(
                    self.converge_func))
        else:
            self.converge_func = self.converge_func.lower()
            if self.converge_func not in ['diff', 'abs', 'weight_diff']:
                raise ValueError(
                    "logistic_param's converge_func not supported, converge_func should be"
                    " 'diff' or 'abs'")

        if type(self.party_weight).__name__ not in ["int", 'float']:
            raise ValueError(
                "logistic_param's party_weight {} not supported, should be 'int' or 'float'".format(
                    self.party_weight))

        if type(self.decay).__name__ not in ["int", 'float']:
            raise ValueError(
                "logistic_param's decay {} not supported, should be 'int' or 'float'".format(
                    self.decay))

        if type(self.decay_sqrt).__name__ not in ['bool']:
            raise ValueError(
                "logistic_param's decay_sqrt {} not supported, should be 'bool'".format(
                    self.decay_sqrt))
        return True


class HomoLogisticParam(LogisticParam):
    """
    Parameters
    ----------
    re_encrypt_batches : int, default: 2
        Required when using encrypted version HomoLR. Since multiple batch updating coefficient may cause
        overflow error. The model need to be re-encrypt for every several batches. Please be careful when setting
        this parameter. Too large batches may cause training failure.

    aggregate_iters : int, default: 1
        Indicate how many iterations are aggregated once.

    """
    def __init__(self, penalty='L2',
                 eps=1e-5, alpha=1.0, optimizer='sgd', party_weight=1,
                 batch_size=-1, learning_rate=0.01, init_param=InitParam(),
                 max_iter=100, converge_func='diff',
                 encrypt_param=EncryptParam(), re_encrypt_batches=2,
                 predict_param=PredictParam(), cv_param=CrossValidationParam(),
                 one_vs_rest_param=OneVsRestParam(), decay=1, decay_sqrt=True,
                 aggregate_iters=1
                 ):
        super(HomoLogisticParam, self).__init__(penalty=penalty, eps=eps, alpha=alpha, optimizer=optimizer,
                                                party_weight=party_weight, batch_size=batch_size,
                                                learning_rate=learning_rate,
                                                init_param=init_param, max_iter=max_iter, converge_func=converge_func,
                                                predict_param=predict_param, cv_param=cv_param,
                                                one_vs_rest_param=one_vs_rest_param, decay=decay, decay_sqrt=decay_sqrt)

        self.encrypt_param = copy.deepcopy(encrypt_param)
        self.re_encrypt_batches = re_encrypt_batches
        self.aggregate_iters = aggregate_iters

    def check(self):
        super().check()
        self.encrypt_param.check()
        if type(self.re_encrypt_batches).__name__ != "int":
            raise ValueError(
                "logistic_param's re_encrypt_batches {} not supported, should be int type".format(
                    self.re_encrypt_batches))
        elif self.re_encrypt_batches < 0:
            raise ValueError(
                "logistic_param's re_encrypt_batches must be greater or equal to 0")

        if not isinstance(self.aggregate_iters, int):
            raise ValueError(
                "logistic_param's aggregate_iters {} not supported, should be int type".format(
                    self.aggregate_iters))

        if self.encrypt_param.method == consts.PAILLIER:
            if self.optimizer != 'sgd':
                raise ValueError("Paillier encryption mode supports 'sgd' optimizer method only.")

        return True


class HeteroLogisticParam(LogisticParam):
    def __init__(self, penalty='L2',
                 eps=1e-5, alpha=1.0, optimizer='sgd', party_weight=1,
                 batch_size=-1, learning_rate=0.01, init_param=InitParam(),
                 max_iter=100, converge_func='diff',
                 encrypted_mode_calculator_param=EncryptedModeCalculatorParam(),
                 predict_param=PredictParam(), cv_param=CrossValidationParam(),
                 one_vs_rest_param=OneVsRestParam(), decay=1, decay_sqrt=True
                 ):
        super(HeteroLogisticParam, self).__init__(penalty=penalty, eps=eps, alpha=alpha, optimizer=optimizer,
                                                  party_weight=party_weight, batch_size=batch_size,
                                                  learning_rate=learning_rate,
                                                  init_param=init_param, max_iter=max_iter, converge_func=converge_func,
                                                  predict_param=predict_param, cv_param=cv_param,
                                                  one_vs_rest_param=one_vs_rest_param, decay=decay,
                                                  decay_sqrt=decay_sqrt)
        self.encrypted_mode_calculator_param = encrypted_mode_calculator_param

    def check(self):
        super().check()
        self.encrypted_mode_calculator_param.check()
        return True