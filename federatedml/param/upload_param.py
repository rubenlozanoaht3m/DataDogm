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


class UploadParam:
    def __init__(self, file="", head=1, partition=10,
                 namespace="", table_name="",
                 data_type="", gen_table_info=False, work_mode=0):
        self.file = file
        self.head = head
        self.partition = partition
        self.namespace = namespace
        self.table_name = table_name
        self.data_type = data_type
        self.gen_tabel_info = gen_table_info
        self.work_mode = work_mode

    def check(self):
        return True

