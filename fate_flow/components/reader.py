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
import uuid

from fate_flow.manager.table_manager.table_convert import convert
from fate_flow.entity.metric import MetricMeta

from arch.api.utils import log_utils
from fate_flow.manager.table_manager.table_operation import get_table
from fate_flow.utils.job_utils import generate_session_id

LOGGER = log_utils.getLogger()


class Reader(object):
    def __init__(self):
        self.data_output = None
        self.task_id = ''
        self.tracker = None
        self.parameters = None

    def run(self, component_parameters=None, args=None):
        self.parameters = component_parameters["ReaderParam"]
        job_id = generate_session_id(self.task_id, self.tracker.role, self.tracker.party_id)
        data_name = [key for key in self.parameters.keys()][0]
        data_table = get_table(job_id=job_id,
                               namespace=self.parameters[data_name]['namespace'],
                               name=self.parameters[data_name]['name']
                               )
        persistent_table_namespace, persistent_table_name = 'output_data_{}'.format(self.task_id), uuid.uuid1().hex
        table = convert(data_table, job_id=generate_session_id(self.task_id, self.tracker.role, self.tracker.party_id),
                        name=persistent_table_name, namespace=persistent_table_namespace, force=True)
        if not table:
            persistent_table_name = data_table.get_name()
            persistent_table_namespace = data_table.get_namespace()
        partitions = data_table.get_partitions()
        count = data_table.count()
        LOGGER.info('save data view:name {}, namespace {}, partitions {}, count {}'.format(persistent_table_name,
                                                                                           persistent_table_namespace,
                                                                                           partitions,
                                                                                           count))
        self.tracker.save_data_view(
            data_info={'f_table_name':  persistent_table_name,
                       'f_table_namespace':  persistent_table_namespace,
                       'f_partition': partitions,
                       'f_table_count_actual': count,
                       'f_data_name':data_name},
            mark=True)
        self.callback_metric(metric_name='reader_name',
                             metric_namespace='reader_namespace',
                             data_info={"count": count,
                                        "partitions": partitions,
                                        "input_table_storage_engine": data_table.get_storage_engine(),
                                        "output_table_storage_engine": table.get_storage_engine() if table else
                                        data_table.get_storage_engine()}
                             )

    def set_taskid(self, taskid):
        self.task_id = taskid

    def set_tracker(self, tracker):
        self.tracker = tracker

    def save_data(self):
        return None

    def export_model(self):
        return None

    def callback_metric(self, metric_name, metric_namespace, data_info):
        self.tracker.set_metric_meta(metric_namespace,
                                     metric_name,
                                     MetricMeta(name='reader',
                                                metric_type='data_info',
                                                extra_metas=data_info))

