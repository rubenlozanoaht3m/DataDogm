from typing import List
import functools
import copy
import numpy as np
from scipy import sparse as sp
from federatedml.util import LOGGER
from federatedml.util import consts
from federatedml.feature.fate_element_type import NoneType
from federatedml.util.io_check import assert_io_num_rows_equal
from federatedml.util.anonymous_generator import generate_anonymous
from federatedml.ensemble.basic_algorithms import HeteroDecisionTreeHost
from federatedml.ensemble.boosting import HeteroBoostingHost
from federatedml.param.boosting_param import HeteroSecureBoostParam, DecisionTreeParam
from federatedml.transfer_variable.transfer_class.hetero_secure_boosting_predict_transfer_variable import \
    HeteroSecureBoostTransferVariable
from federatedml.ensemble.secureboost.secureboost_util.tree_model_io import produce_hetero_tree_learner, \
    load_hetero_tree_learner
from federatedml.ensemble.secureboost.secureboost_util.boosting_tree_predict import sbt_host_predict, \
    mix_sbt_host_predict
from federatedml.protobuf.generated.boosting_tree_model_meta_pb2 import BoostingTreeModelMeta
from federatedml.protobuf.generated.boosting_tree_model_meta_pb2 import QuantileMeta
from federatedml.protobuf.generated.boosting_tree_model_param_pb2 import BoostingTreeModelParam
from federatedml.ensemble.secureboost.secureboost_util import hetero_fast_secureboost_plan as plan


class HeteroSecureBoostingTreeHost(HeteroBoostingHost):

    def __init__(self):
        super(HeteroSecureBoostingTreeHost, self).__init__()
        self.use_missing = False
        self.zero_as_missing = False
        self.cur_epoch_idx = -1
        self.grad_and_hess = None
        self.tree_param = DecisionTreeParam()  # decision tree param
        self.model_param = HeteroSecureBoostParam()
        self.complete_secure = False
        self.model_name = 'HeteroSecureBoost'
        self.enable_goss = False
        self.cipher_compressing = False
        self.max_sample_weight = None
        self.round_decimal = None
        self.new_ver = True

        self.work_mode = consts.STD_TREE

        # fast sbt param
        self.tree_num_per_party = 1
        self.guest_depth = 0
        self.host_depth = 0
        self.init_tree_plan = False
        self.tree_plan = []

        self.predict_transfer_inst = HeteroSecureBoostTransferVariable()

    def _init_model(self, param: HeteroSecureBoostParam):

        super(HeteroSecureBoostingTreeHost, self)._init_model(param)
        self.tree_param = param.tree_param
        self.use_missing = param.use_missing
        self.enable_goss = param.run_goss
        self.zero_as_missing = param.zero_as_missing
        self.complete_secure = param.complete_secure
        self.sparse_opt_para = param.sparse_optimization
        self.cipher_compressing = param.cipher_compress
        self.new_ver = param.new_ver

        self.tree_num_per_party = param.tree_num_per_party
        self.work_mode = param.work_mode
        self.guest_depth = param.guest_depth
        self.host_depth = param.host_depth

        if self.use_missing:
            self.tree_param.use_missing = self.use_missing
            self.tree_param.zero_as_missing = self.zero_as_missing

    def get_tree_plan(self, idx):

        if not self.init_tree_plan:
            tree_plan = plan.create_tree_plan(self.work_mode, k=self.tree_num_per_party, tree_num=self.boosting_round,
                                              host_list=self.component_properties.host_party_idlist,
                                              complete_secure=self.complete_secure)
            self.tree_plan += tree_plan
            self.init_tree_plan = True

        LOGGER.info('tree plan is {}'.format(self.tree_plan))
        return self.tree_plan[idx]

    def fit_a_booster(self, epoch_idx: int, booster_dim: int):

        flow_id = self.generate_flowid(epoch_idx, booster_dim)
        complete_secure = True if (self.cur_epoch_idx == 0 and self.complete_secure) else False
        fast_sbt = (self.work_mode != consts.STD_TREE)

        tree_type, target_host_id = None, None
        if fast_sbt:
            tree_type, target_host_id = self.get_tree_plan(epoch_idx)

        tree = produce_hetero_tree_learner(role=self.role, tree_param=self.tree_param, flow_id=flow_id,
                                           data_bin=self.data_bin, bin_split_points=self.bin_split_points,
                                           bin_sparse_points=self.bin_sparse_points, task_type=self.task_type,
                                           valid_features=self.sample_valid_features(),
                                           host_party_list=self.component_properties.host_party_idlist,
                                           runtime_idx=self.component_properties.local_partyid,
                                           cipher_compress=self.cipher_compressing,
                                           complete_secure=complete_secure,
                                           fast_sbt=fast_sbt, tree_type=tree_type, target_host_id=target_host_id,
                                           guest_depth=self.guest_depth, host_depth=self.host_depth
                                           )

        tree.fit()

        return tree

    def load_booster(self, model_meta, model_param, epoch_idx, booster_idx):

        flow_id = self.generate_flowid(epoch_idx, booster_idx)
        runtime_idx = self.component_properties.local_partyid
        fast_sbt = (self.work_mode != consts.STD_TREE)
        tree_type, target_host_id = None, None

        if fast_sbt:
            tree_type, target_host_id = self.get_tree_plan(epoch_idx)

        tree = load_hetero_tree_learner(self.role, self.tree_param, model_meta, model_param, flow_id,
                                        runtime_idx,
                                        fast_sbt=fast_sbt, tree_type=tree_type, target_host_id=target_host_id)

        return tree

    def generate_summary(self) -> dict:

        summary = {'best_iteration': self.callback_variables.best_iteration, 'is_converged': self.is_converged}

        LOGGER.debug('summary is {}'.format(summary))

        return summary

    @staticmethod
    def traverse_a_tree(tree: HeteroDecisionTreeHost, sample, cur_node_idx):

        nid, _ = tree.traverse_tree(predict_state=(cur_node_idx, -1), data_inst=sample,
                                    decoder=tree.decode, split_maskdict=tree.split_maskdict,
                                    missing_dir_maskdict=tree.missing_dir_maskdict, sitename=tree.sitename,
                                    tree_=tree.tree_node, zero_as_missing=tree.zero_as_missing,
                                    use_missing=tree.use_missing)

        return nid, _

    @staticmethod
    def traverse_trees(leaf_pos, sample, trees: List[HeteroDecisionTreeHost]):

        for t_idx, tree in enumerate(trees):

            cur_node_idx = leaf_pos['node_pos'][t_idx]
            # idx is set as -1 when a sample reaches leaf
            if cur_node_idx == -1:
                continue
            nid, _ = HeteroSecureBoostingTreeHost.traverse_a_tree(tree, sample, cur_node_idx)
            leaf_pos['node_pos'][t_idx] = nid

        return leaf_pos

    def boosting_fast_predict(self, data_inst, trees: List[HeteroDecisionTreeHost]):

        comm_round = 0

        traverse_func = functools.partial(self.traverse_trees, trees=trees)

        while True:

            LOGGER.debug('cur predict round is {}'.format(comm_round))

            stop_flag = self.predict_transfer_inst.predict_stop_flag.get(idx=0, suffix=(comm_round, ))
            if stop_flag:
                break

            guest_node_pos = self.predict_transfer_inst.guest_predict_data.get(idx=0, suffix=(comm_round, ))
            host_node_pos = guest_node_pos.join(data_inst, traverse_func)
            if guest_node_pos.count() != host_node_pos.count():
                raise ValueError('sample count mismatch: guest table {}, host table {}'.format(guest_node_pos.count(),
                                                                                               host_node_pos.count()))
            self.predict_transfer_inst.host_predict_data.remote(host_node_pos, idx=-1, suffix=(comm_round, ))

            comm_round += 1

    @assert_io_num_rows_equal
    def predict(self, data_inst):

        LOGGER.info('running prediction')

        processed_data = self.data_and_header_alignment(data_inst)

        predict_start_round = self.sync_predict_start_round()

        rounds = len(self.boosting_model_list) // self.booster_dim
        trees = []
        for idx in range(predict_start_round, rounds):
            for booster_idx in range(self.booster_dim):
                tree = self.load_booster(self.booster_meta,
                                         self.boosting_model_list[idx * self.booster_dim + booster_idx],
                                         idx, booster_idx)
                trees.append(tree)

        if len(trees) == 0:
            LOGGER.info('no tree for predicting, prediction done')
            return

        if self.work_mode == consts.MIX_TREE:
            mix_sbt_host_predict(processed_data, self.predict_transfer_inst, trees)
        else:
            sbt_host_predict(processed_data, self.predict_transfer_inst, trees)

    def get_model_meta(self):
        model_meta = BoostingTreeModelMeta()
        model_meta.tree_meta.CopyFrom(self.booster_meta)
        model_meta.num_trees = self.boosting_round
        model_meta.quantile_meta.CopyFrom(QuantileMeta(bin_num=self.bin_num))
        model_meta.work_mode = self.work_mode
        meta_name = "HeteroSecureBoostingTreeHostMeta"
        return meta_name, model_meta

    def get_model_param(self):

        model_param = BoostingTreeModelParam()
        model_param.tree_num = len(self.boosting_model_list)
        model_param.tree_dim = self.booster_dim
        model_param.trees_.extend(self.boosting_model_list)

        anonymous_name_mapping = {}
        party_id = self.component_properties.local_partyid
        for fid, name in self.feature_name_fid_mapping.items():
            anonymous_name_mapping[generate_anonymous(fid, role=consts.HOST, party_id=party_id,)] = name

        model_param.anonymous_name_mapping.update(anonymous_name_mapping)
        model_param.feature_name_fid_mapping.update(self.feature_name_fid_mapping)
        model_param.model_name = consts.HETERO_SBT

        model_param.anonymous_name_mapping.update(anonymous_name_mapping)
        model_param.feature_name_fid_mapping.update(self.feature_name_fid_mapping)
        model_param.model_name = consts.HETERO_SBT
        model_param.best_iteration = self.callback_variables.best_iteration
        model_param.tree_plan.extend(plan.encode_plan(self.tree_plan))
        
        param_name = "HeteroSecureBoostingTreeHostParam"

        return param_name, model_param

    def set_model_meta(self, model_meta):
        if not self.is_warm_start:
            self.boosting_round = model_meta.num_trees
        self.booster_meta = model_meta.tree_meta
        self.bin_num = model_meta.quantile_meta.bin_num
        self.work_mode = model_meta.work_mode

    def set_model_param(self, model_param):
        self.boosting_model_list = list(model_param.trees_)
        self.booster_dim = model_param.tree_dim
        self.feature_name_fid_mapping.update(model_param.feature_name_fid_mapping)
        self.tree_plan = plan.decode_plan(model_param.tree_plan)