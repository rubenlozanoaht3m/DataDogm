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
################################################################################
#
#
################################################################################

# =============================================================================
# FeatureHistogram
# =============================================================================
import copy
import functools
import uuid
from operator import add, sub
from typing import List

from fate_arch.session import computing_session as session
from fate_arch.common import log
from federatedml.feature.fate_element_type import NoneType
from federatedml.framework.weights import Weights

LOGGER = log.getLogger()


class HistogramBag(object):

    """
    holds histograms
    """

    def __init__(self, tensor: list, hid: int = -1, p_hid: int = -1):

        """
        :param tensor: list returned by calculate_histogram
        :param hid: histogram id
        :param p_hid: parent node histogram id
        """

        self.hid = hid
        self.p_hid = p_hid
        self.bag = tensor

    def binary_op(self, other, func, inplace=False):
        assert isinstance(other, HistogramBag)
        assert len(self.bag) == len(other)

        bag = self.bag
        newbag = None
        if not inplace:
            newbag = copy.deepcopy(other)
            bag = newbag.bag

        for bag_idx in range(len(self.bag)):
            for hist_idx in range(len(self.bag[bag_idx])):
                bag[bag_idx][hist_idx][0] = func(self.bag[bag_idx][hist_idx][0], other[bag_idx][hist_idx][0])
                bag[bag_idx][hist_idx][1] = func(self.bag[bag_idx][hist_idx][1], other[bag_idx][hist_idx][1])
                bag[bag_idx][hist_idx][2] = func(self.bag[bag_idx][hist_idx][2], other[bag_idx][hist_idx][2])

        return self if inplace else newbag

    def from_hist_tensor(self):
        pass

    def __add__(self, other):
        return self.binary_op(other, add, inplace=False)

    def __sub__(self, other):
        return self.binary_op(other, sub, inplace=False)

    def __len__(self):
        return len(self.bag)

    def __getitem__(self, item):
        return self.bag[item]

    def __str__(self):
        return str(self.bag)


class FeatureHistogramWeights(Weights):

    def __init__(self, list_of_histogram_bags: List[HistogramBag]):

        self.hists = list_of_histogram_bags
        super(FeatureHistogramWeights, self).__init__(l=list_of_histogram_bags)

    def map_values(self, func, inplace):

        if inplace:
            hists = self.hists
        else:
            hists = copy.deepcopy(self.hists)

        for histbag in hists:
            bag = histbag.bag
            for component_idx in range(len(bag)):
                for hist_idx in range(len(bag[component_idx])):
                    bag[component_idx][hist_idx][0] = func(bag[component_idx][hist_idx][0])
                    bag[component_idx][hist_idx][1] = func(bag[component_idx][hist_idx][1])
                    bag[component_idx][hist_idx][2] = func(bag[component_idx][hist_idx][2])

        if inplace:
            return self
        else:
            return FeatureHistogramWeights(list_of_histogram_bags=hists)

    def binary_op(self, other: 'FeatureHistogramWeights', func, inplace:bool):

        new_weights = []
        hists, other_hists = self.hists, other.hists
        for h1, h2 in zip(hists, other_hists):
            rnt = h1.binary_op(h2, func, inplace=inplace)
            if not inplace:
                new_weights.append(rnt)

        if inplace:
            return self
        else:
            return FeatureHistogramWeights(new_weights)

    def axpy(self, a, y: 'FeatureHistogramWeights'):

        func = lambda x1, x2: x1 + a*x2
        self.binary_op(y, func, inplace=True)

        return self

    def __iter__(self):
        pass

    def __str__(self):
        return str([str(hist) for hist in self.hists])


class FeatureHistogram(object):

    def __init__(self):
        pass

    @staticmethod
    def guest_accumulate_histogram(histograms, ):
        for i in range(1, len(histograms)):
            for j in range(len(histograms[i])):
                histograms[i][j] += histograms[i - 1][j]
        return histograms

    @staticmethod
    def host_accumulate_histogram_0(histograms, ):
        new_hist = copy.deepcopy(histograms)
        for i in range(1, len(new_hist)):
            for j in range(len(new_hist[i])):
                new_hist[i][j] += new_hist[i - 1][j]
        return new_hist

    @staticmethod
    def host_accumulate_histogram_1(histograms, ):

        new_hist = [[0, 0, 0] for i in range(len(histograms))]
        new_hist[0][0] = copy.deepcopy(histograms[0][0])
        new_hist[0][1] = copy.deepcopy(histograms[0][1])
        new_hist[0][2] = copy.deepcopy(histograms[0][2])

        for i in range(1, len(histograms)):
            for j in range(len(histograms[i])):
                new_hist[i][j] = new_hist[i - 1][j] + histograms[i][j]
        return new_hist

    @staticmethod
    def host_accumulate_histogram_map_func(k, v):

        nid, fid = k
        histograms = v
        new_value = (fid, FeatureHistogram.host_accumulate_histogram_0(histograms))
        return k, new_value

    @staticmethod
    def calculate_histogram(data_bin, grad_and_hess,
                            bin_split_points, bin_sparse_points,
                            valid_features=None, node_map=None,
                            use_missing=False, zero_as_missing=False, ret="tensor"):
        LOGGER.info("bin_shape is {}, node num is {}".format(bin_split_points.shape, len(node_map)),)

        batch_histogram_cal = functools.partial(
            FeatureHistogram.batch_calculate_histogram,
            bin_split_points=bin_split_points, bin_sparse_points=bin_sparse_points,
            valid_features=valid_features, node_map=node_map,
            use_missing=use_missing, zero_as_missing=zero_as_missing)

        agg_histogram = functools.partial(FeatureHistogram.aggregate_histogram, node_map=node_map)

        # batch_histogram = data_bin.join(grad_and_hess, \
        #                                 lambda data_inst, g_h: (data_inst, g_h)).mapPartitions2(batch_histogram_cal)

        batch_histogram_intermediate_rs = data_bin.join(grad_and_hess, lambda data_inst, g_h: (data_inst, g_h))
        import time
        s = time.time()
        histograms_table = batch_histogram_intermediate_rs.mapReducePartitions(batch_histogram_cal, agg_histogram)
        e = time.time()
        LOGGER.debug('map reduce takes {}'.format(e-s))
        # histograms_dict = batch_histogram.reduce(agg_histogram, key_func=lambda key: (key[1], key[2]))

        if ret == "tensor":
            feature_num = bin_split_points.shape[0]
            rs = FeatureHistogram.recombine_histograms(histograms_table, node_map, feature_num)
            return rs
        else:
            return FeatureHistogram.construct_table(histograms_table, )


    @staticmethod
    def aggregate_histogram(histogram1, histogram2, node_map=None):
        for i in range(len(histogram1)):
            for j in range(len(histogram1[i])):
                histogram1[i][j] += histogram2[i][j]

        return histogram1

    @staticmethod
    def batch_calculate_histogram(kv_iterator, bin_split_points=None,
                                  bin_sparse_points=None, valid_features=None,
                                  node_map=None, use_missing=False, zero_as_missing=False):
        data_bins = []
        node_ids = []
        grad = []
        hess = []

        data_record = 0

        for _, value in kv_iterator:
            data_bin, nodeid_state = value[0]
            unleaf_state, nodeid = nodeid_state
            if unleaf_state == 0 or nodeid not in node_map:
                continue
            g, h = value[1]
            data_bins.append(data_bin)
            node_ids.append(nodeid)
            grad.append(g)
            hess.append(h)

            data_record += 1

        LOGGER.info("begin batch calculate histogram, data count is {}".format(data_record))
        node_num = len(node_map)

        missing_bin = 1 if use_missing else 0
        zero_optim = [[[0 for i in range(3)]
                       for j in range(bin_split_points.shape[0])]
                      for k in range(node_num)]
        zero_opt_node_sum = [[0 for i in range(3)]
                             for j in range(node_num)]

        node_histograms = []
        for k in range(node_num):
            feature_histogram_template = []
            for fid in range(bin_split_points.shape[0]):
                if valid_features is not None and valid_features[fid] is False:
                    feature_histogram_template.append([])
                    continue
                else:
                    feature_histogram_template.append([[0 for i in range(3)]
                                                       for j in
                                                       range(bin_split_points[fid].shape[0] + 1 + missing_bin)])

            node_histograms.append(feature_histogram_template)

        assert len(feature_histogram_template) == bin_split_points.shape[0]

        for rid in range(data_record):
            nid = node_map.get(node_ids[rid])
            zero_opt_node_sum[nid][0] += grad[rid]
            zero_opt_node_sum[nid][1] += hess[rid]
            zero_opt_node_sum[nid][2] += 1
            for fid, value in data_bins[rid].features.get_all_data():
                if valid_features is not None and valid_features[fid] is False:
                    continue

                if use_missing and value == NoneType():
                    value = -1

                node_histograms[nid][fid][value][0] += grad[rid]
                node_histograms[nid][fid][value][1] += hess[rid]
                node_histograms[nid][fid][value][2] += 1

                zero_optim[nid][fid][0] += grad[rid]
                zero_optim[nid][fid][1] += hess[rid]
                zero_optim[nid][fid][2] += 1

        for nid in range(node_num):
            for fid in range(bin_split_points.shape[0]):
                if valid_features is not None and valid_features[fid] is True:
                    if not use_missing or (use_missing and not zero_as_missing):
                        sparse_point = bin_sparse_points[fid]
                        node_histograms[nid][fid][sparse_point][0] += zero_opt_node_sum[nid][0] - zero_optim[nid][fid][
                            0]
                        node_histograms[nid][fid][sparse_point][1] += zero_opt_node_sum[nid][1] - zero_optim[nid][fid][
                            1]
                        node_histograms[nid][fid][sparse_point][2] += zero_opt_node_sum[nid][2] - zero_optim[nid][fid][
                            2]
                    else:
                        node_histograms[nid][fid][-1][0] += zero_opt_node_sum[nid][0] - zero_optim[nid][fid][0]
                        node_histograms[nid][fid][-1][1] += zero_opt_node_sum[nid][1] - zero_optim[nid][fid][1]
                        node_histograms[nid][fid][-1][2] += zero_opt_node_sum[nid][2] - zero_optim[nid][fid][2]

        ret = []
        for nid in range(node_num):
            for fid in range(bin_split_points.shape[0]):
                ret.append(((nid, fid), node_histograms[nid][fid]))

        return ret

    @staticmethod
    def recombine_histograms(histograms_table, node_map, feature_num):

        histograms = [[[] for j in range(feature_num)] for k in range(len(node_map))]
        histogram_list = list(histograms_table.collect())
        for tuple_ in histogram_list:
            nid, fid = tuple_[0]
            histograms[int(nid)][int(fid)] = FeatureHistogram.guest_accumulate_histogram(tuple_[1])
        LOGGER.debug('hist table is {}'.format(histograms))
        return histograms

    @staticmethod
    def construct_table(histograms_table,):
        histograms_table = histograms_table.map(FeatureHistogram.host_accumulate_histogram_map_func)
        return histograms_table




