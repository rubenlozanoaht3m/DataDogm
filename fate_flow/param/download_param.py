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


class DownloadParam:
    def __init__(self, output_path="", delimitor=",",
                 namespace="", name="", work_mode=0):
        self.output_path = output_path
        self.delimitor = delimitor
        self.namespace = namespace
        self.name = name
        self.work_mode = work_mode

    def check(self):
        return True