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

from pipeline.param.base_param import BaseParam
from pipeline.param.cross_validation_param import CrossValidationParam
from pipeline.param.encrypt_param import EncryptParam
from pipeline.param.encrypted_mode_calculation_param import EncryptedModeCalculatorParam
from pipeline.param.init_model_param import InitParam
from pipeline.param.predict_param import PredictParam
from pipeline.param.stepwise_param import StepwiseParam
from pipeline.param.sqn_param import StochasticQuasiNewtonParam
from pipeline.param.callback_param import CallbackParam
from pipeline.param import consts


class LogisticParam(BaseParam):
    """
    Parameters used for Logistic Regression both for Homo mode or Hetero mode.

    Parameters
    ----------
    penalty : {'L2', 'L1' or None}
        Penalty method used in LR. Please note that, when using encrypted version in HomoLR,
        'L1' is not supported.

    tol : float, default: 1e-4
        The tolerance of convergence

    alpha : float, default: 1.0
        Regularization strength coefficient.

    optimizer : {'rmsprop', 'sgd', 'adam', 'nesterov_momentum_sgd', 'adagrad'}, default: 'rmsprop'
        Optimize method.

    batch_size : int, default: -1
        Batch size when updating model. -1 means use all data in a batch. i.e. Not to use mini-batch strategy.

    learning_rate : float, default: 0.01
        Learning rate

    max_iter : int, default: 100
        The maximum iteration for training.

    early_stop : {'diff', 'weight_diff', 'abs'}, default: 'diff'
        Method used to judge converge or not.
            a)	diff： Use difference of loss between two iterations to judge whether converge.
            b)  weight_diff: Use difference between weights of two consecutive iterations
            c)	abs: Use the absolute value of loss to judge whether converge. i.e. if loss < eps, it is converged.

            Please note that for hetero-lr multi-host situation, this parameter support "weight_diff" only.

    decay: int or float, default: 1
        Decay rate for learning rate. learning rate will follow the following decay schedule.
        lr = lr0/(1+decay*t) if decay_sqrt is False. If decay_sqrt is True, lr = lr0 / sqrt(1+decay*t)
        where t is the iter number.

    decay_sqrt: bool, default: True
        lr = lr0/(1+decay*t) if decay_sqrt is False, otherwise, lr = lr0 / sqrt(1+decay*t)

    encrypt_param: EncryptParam object, default: default EncryptParam object
        encrypt param

    predict_param: PredictParam object, default: default PredictParam object
        predict param

    callback_param: CallbackParam object
        callback param

    cv_param: CrossValidationParam object, default: default CrossValidationParam object
        cv param

    multi_class: {'ovr'}, default: 'ovr'
        If it is a multi_class task, indicate what strategy to use. Currently, support 'ovr' short for one_vs_rest only.

    validation_freqs: int or list or tuple or set, or None, default None
        validation frequency during training.

    early_stopping_rounds: int, default: None
        Will stop training if one metric doesn’t improve in last early_stopping_round rounds

    metrics: list or None, default: None
        Indicate when executing evaluation during train process, which metrics will be used. If set as empty,
        default metrics for specific task type will be used. As for binary classification, default metrics are
        ['auc', 'ks']

    use_first_metric_only: bool, default: False
        Indicate whether use the first metric only for early stopping judgement.

    floating_point_precision: None or integer
        if not None, use floating_point_precision-bit to speed up calculation,
        e.g.: convert an x to round(x * 2**floating_point_precision) during Paillier operation, divide
                the result by 2**floating_point_precision in the end.

    """

    def __init__(self, penalty='L2',
                 tol=1e-4, alpha=1.0, optimizer='rmsprop',
                 batch_size=-1, shuffle=True, batch_strategy="full", masked_rate=5,
                 learning_rate=0.01, init_param=InitParam(),
                 max_iter=100, early_stop='diff', encrypt_param=EncryptParam(),
                 predict_param=PredictParam(), cv_param=CrossValidationParam(),
                 decay=1, decay_sqrt=True,
                 multi_class='ovr', validation_freqs=None, early_stopping_rounds=None,
                 stepwise_param=StepwiseParam(), floating_point_precision=23,
                 metrics=None,
                 use_first_metric_only=False,
                 callback_param=CallbackParam()
                 ):
        super(LogisticParam, self).__init__()
        self.penalty = penalty
        self.tol = tol
        self.alpha = alpha
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.batch_strategy = batch_strategy
        self.masked_rate = masked_rate
        self.learning_rate = learning_rate
        self.init_param = copy.deepcopy(init_param)
        self.max_iter = max_iter
        self.early_stop = early_stop
        self.encrypt_param = encrypt_param
        self.predict_param = copy.deepcopy(predict_param)
        self.cv_param = copy.deepcopy(cv_param)
        self.decay = decay
        self.decay_sqrt = decay_sqrt
        self.multi_class = multi_class
        self.validation_freqs = validation_freqs
        self.stepwise_param = copy.deepcopy(stepwise_param)
        self.early_stopping_rounds = early_stopping_rounds
        self.metrics = metrics or []
        self.use_first_metric_only = use_first_metric_only
        self.floating_point_precision = floating_point_precision
        self.callback_param = copy.deepcopy(callback_param)

    def check(self):
        return True
