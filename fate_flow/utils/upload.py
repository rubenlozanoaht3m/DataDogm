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

import csv
import os
import time

from arch.api import session

from arch.api.utils import log_utils, file_utils, dtable_utils

LOGGER = log_utils.getLogger()


class Upload(object):
    def __init__(self):
        self.taskid = ''
        self.tracker = None
        self.MAX_PARTITION_NUM = 1024
        self.MAX_BYTES = 10240
        self.parameters = {}

    def run(self, component_parameters=None, args=None):
        self.parameters = component_parameters["UploadParam"]
        self.parameters["role"] = component_parameters["role"]
        self.parameters["local"] = component_parameters["local"]
        if not os.path.isabs(self.parameters.get("file", "")):
            self.parameters["file"] = os.path.join(file_utils.get_project_base_directory(), self.parameters["file"])
        if not os.path.exists(self.parameters["file"]):
            raise Exception("%s is not exist, please check the configure" % (self.parameters["file"]))
        table_name, namespace = dtable_utils.get_table_info(config=self.parameters,
                                                            create=True)
        _namespace, _table_name = self.generate_table_name(self.parameters["file"])
        if namespace is None:
            namespace = _namespace
        if table_name is None:
            table_name = _table_name
        read_head = self.parameters['head']
        if read_head == 0:
            head = False
        elif read_head == 1:
            head = True
        else:
            raise Exception("'head' in conf.json should be 0 or 1")
        partition = self.parameters["partition"]
        if partition <= 0 or partition >= self.MAX_PARTITION_NUM:
            raise Exception("Error number of partition, it should between %d and %d" % (0, self.MAX_PARTITION_NUM))

        session.init(mode=self.parameters['work_mode'])
        data_table_count = self.save_data_table(table_name, namespace, head)
        LOGGER.info("------------load data finish!-----------------")
        LOGGER.info("file: {}".format(self.parameters["file"]))
        LOGGER.info("total data_count: {}".format(data_table_count))
        LOGGER.info("table name: {}, table namespace: {}".format(table_name, namespace))

    def set_taskid(self, taskid):
        self.taskid = taskid

    def set_tracker(self, tracker):
        self.tracker = tracker

    def save_data_table(self, dst_table_name, dst_table_namespace, head=True):
        input_file = self.parameters["file"]
        with open(input_file, 'r') as fin:
            if head is True:
                data_head = fin.readline()
                self.save_data_header(data_head, dst_table_name, dst_table_namespace)
            while True:
                data = list()
                lines = fin.readlines(self.MAX_BYTES)
                if lines:
                    for line in lines:
                        values = line.replace("\n", "").replace("\t", ",").split(",")
                        data.append((values[0], self.list_to_str(values[1:])))
                    data_table = session.save_data(data, name=dst_table_name, namespace=dst_table_namespace,
                                                   partition=self.parameters["partition"])

                else:
                    return data_table.count()

    def save_data_header(self, header_source, dst_table_name, dst_table_namespace):
        header_source_item = header_source.split(',')
        session.save_data_table_meta({'header': ','.join(header_source_item[1:]).strip(), 'sid': header_source_item[0]},
                                     dst_table_name,
                                     dst_table_namespace)


    def list_to_str(self, input_list):
        return ','.join(list(map(str, input_list)))

    def generate_table_name(self, input_file_path):
        str_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        file_name = input_file_path.split(".")[0]
        file_name = file_name.split("/")[-1]
        return file_name, str_time

    def save_data(self):
        return None

    def export_model(self):
        return None