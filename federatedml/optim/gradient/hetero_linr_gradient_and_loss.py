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

from arch.api.utils import log_utils
from federatedml.framework.hetero.sync import loss_sync
from federatedml.optim.gradient import hetero_gradient_sync
from federatedml.util.fate_operator import reduce_add

LOGGER = log_utils.getLogger()


class Guest(hetero_gradient_sync.Guest, loss_sync.Guest):
    def __init__(self):
        self.host_forwards = None
        self.wx = None
        self.aggregated_wx = None

    def register_gradient_procedure(self, transfer_variables):
        self._register_gradient_sync(transfer_variables.host_forward,
                                     transfer_variables.fore_gradient,
                                     transfer_variables.guest_gradient,
                                     transfer_variables.guest_optim_gradient)

        self._register_loss_sync(transfer_variables.host_loss_regular,
                                 transfer_variables.loss,
                                 transfer_variables.loss_intermediate)

    def compute_gradient_procedure(self, data_instances, model_weights, encrypted_calculator,
                                   optimizer, n_iter_, batch_index):
        """
        Compute gradients:
        gradient = (1/N)*\sum(wx -y)*x

        Define wx as guest_forward or host_forward
        Define (wx-y) as fore_gradient

        Then, gradient = fore_gradeint * x
        Parameters
        ----------
        data_instances: DTable of Instance, input data

        model_weights: LinearRegressionWeights
            Stores coef_ and intercept_ of lr

        encrypted_calculator: Use for different encrypted methods

        optimizer: optimizer object

        n_iter_: int, current number of iter.

        batch_index: int, use to obtain current encrypted_calculator index:
        """
        current_suffix = (n_iter_, batch_index)

        host_forwards = self.get_host_forward(suffix=current_suffix)
        self.host_forwards = host_forwards
        LOGGER.info("Get host_forwards from host")

        wx = data_instances.mapValues(
            lambda v: np.dot(v.features, model_weights.coef_) + model_weights.intercept_)
        self.wx = wx
        self.aggregated_wx = encrypted_calculator[batch_index].encrypt(wx)

        for host_forward in host_forwards:
            self.aggregated_wx = self.aggregated_wx.join(host_forward, lambda g, h: g + h)
        fore_gradient = self.aggregated_wx.join(data_instances, lambda wx, d: wx - d.label)

        self.remote_fore_gradient(fore_gradient, suffix=current_suffix)
        LOGGER.info("Remote fore_gradient to Host")

        unilateral_gradient = self.compute_gradient(data_instances,
                                                    fore_gradient,
                                                    model_weights.fit_intercept)
        unilateral_gradient = optimizer.add_regular_to_grad(unilateral_gradient, model_weights)
        optimized_gradient = self.update_gradient(unilateral_gradient, suffix=current_suffix)

        return optimized_gradient, fore_gradient, host_forwards

    def compute_loss(self, data_instances, n_iter_, batch_index, loss_norm=None):
        """
        Compute hetero linr loss:
            loss = (1/N)*\sum(wx-y)^2 where y is label, w is model weight and x is features
        (wx - y)^2 = (wx_h)^2 + (wx_g - y)^2 + 2*(wx_h + wx_g - y)
        """
        current_suffix = (n_iter_, batch_index)
        n = data_instances.count()
        self_wx_square = self.wx.mapValues(lambda x: np.square(x)).reduce(reduce_add)
        loss_list = []
        host_wx_squares = self.get_host_loss_intermediate(current_suffix)
        if loss_norm is not None:
            host_loss_regular = self.get_host_loss_regular(suffix=current_suffix)
        else:
            host_loss_regular = []
        for host_idx, host_forward in enumerate(self.host_forwards):
            loss_gh = self.wx.join(host_forward, lambda g, h: g*h).reduce(reduce_add)
            loss = (self_wx_square + host_wx_squares[host_idx] + 2 * loss_gh) / n
            if loss_norm is not None:
                loss = loss + loss_norm
                loss = loss + host_loss_regular[host_idx]
            loss_list.append(loss)
        self.sync_loss_info(loss_list, suffix=current_suffix)

class Host(hetero_gradient_sync.Host, loss_sync.Host):
    def __init__(self):
        self.wx = None

    def register_gradient_procedure(self, transfer_variables):
        self._register_gradient_sync(transfer_variables.host_forward,
                                     transfer_variables.fore_gradient,
                                     transfer_variables.host_gradient,
                                     transfer_variables.host_optim_gradient)
        self._register_loss_sync(transfer_variables.host_loss_regular,
                                 transfer_variables.loss,
                                 transfer_variables.loss_intermediate)

    def compute_gradient_procedure(self, data_instances, model_weights, encrypted_calculator,
                                   optimizer, n_iter_, batch_index):
        """
                Compute gradients:
                gradient = (1/N)*\sum(wx -y)*x

                Define wx as guest_forward or host_forward
                Define (wx-y) as fore_gradient

                Then, gradient = fore_gradeint * x
               Parameters
                ----------
                data_instances: DTable of Instance, input data

                model_weights: LinearRegressionWeights
                    Stores coef_ and intercept_ of lr

                encrypted_calculator: Use for different encrypted methods

                optimizer: optimizer object

                n_iter_: int, current number of iter.

                batch_index: int, use to obtain current encrypted_calculator index:
                """
        current_suffix = (n_iter_, batch_index)

        wx = data_instances.mapValues(lambda v: np.dot(v.features, model_weights.coef_) + model_weights.intercept_)
        self.wx = wx

        host_forward = encrypted_calculator[batch_index].encrypt(wx)
        self.remote_host_forward(host_forward, suffix=current_suffix)

        fore_gradient = self.get_fore_gradient(suffix=current_suffix)

        unilateral_gradient = self.compute_gradient(data_instances,
                                                    fore_gradient,
                                                    model_weights.fit_intercept)
        optimized_gradient = self.update_gradient(unilateral_gradient, suffix=current_suffix)

        return optimized_gradient, fore_gradient

    def compute_loss(self, model_weights, optimizer, n_iter_, batch_index):
        """
        Compute htero linr loss for:
            loss = (1/N)*\sum(wx-y)^2 where y is label, w is model weight and x is features

            Note: (wx - y)^2 = (wx_h)^2 + (wx_g - y)^2 + 2*(wx_h + wx_g - y)
        """

        current_suffix = (n_iter_, batch_index)
        self_wx_square = self.wx.mapValues(lambda x: np.square(x)).reduce(reduce_add)
        self.remote_loss_intermediate(self_wx_square, suffix=current_suffix)

        loss_regular = optimizer.loss_norm(model_weights.coef_)
        self.remote_loss_regular(loss_regular, suffix=current_suffix)


class Arbiter(hetero_gradient_sync.Arbiter, loss_sync.Arbiter):
    def register_gradient_procedure(self, transfer_variables):
        self._register_gradient_sync(transfer_variables.guest_gradient,
                                     transfer_variables.host_gradient,
                                     transfer_variables.guest_optim_gradient,
                                     transfer_variables.host_optim_gradient)
        self._register_loss_sync(transfer_variables.loss)

    def compute_gradient_procedure(self, cipher_operator, optimizer, n_iter_, batch_index):
        """
        Decrypt gradients.

        Parameters
        ----------
        cipher_operator: Use for encryption

        optimizer: optimizer that get delta gradient of this iter

        n_iter_: int, current iter nums

        batch_index: int, use to obtain current encrypted_calculator

        """
        current_suffix = (n_iter_, batch_index)

        host_gradients, guest_gradient = self.get_local_gradient(current_suffix)

        host_gradients = [np.array(h) for h in host_gradients]
        guest_gradient = np.array(guest_gradient)

        size_list = [h_g.shape[0] for h_g in host_gradients]
        size_list.append(guest_gradient.shape[0])

        gradient = np.hstack((h for h in host_gradients))
        gradient = np.hstack((gradient, guest_gradient))

        grad = np.array(cipher_operator.decrypt_list(gradient))
        delta_grad = optimizer.apply_gradients(grad)
        separate_optim_gradient = self.separate(delta_grad, size_list)
        host_optim_gradients = separate_optim_gradient[: -1]
        guest_optim_gradient = separate_optim_gradient[-1]

        self.remote_local_gradient(host_optim_gradients, guest_optim_gradient, current_suffix)
        return delta_grad

    def compute_loss(self, cipher, n_iter_, batch_index):
        """
        Decrypt loss from guest
        """
        current_suffix = (n_iter_, batch_index)
        loss_list = self.sync_loss_info(suffix=current_suffix)
        de_loss_list = cipher.decrypt_list(loss_list)
        return de_loss_list
