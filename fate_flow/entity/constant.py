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
from enum import IntEnum


class WorkMode(IntEnum):
    STANDALONE = 0
    CLUSTER = 1


class Backend(IntEnum):
    EGGROLL = 0
    SPARK = 1

    def is_eggroll(self):
        return self.value == self.EGGROLL

    def is_spark(self):
        return self.value == self.SPARK


class StoreEngine(IntEnum):
    EGGROLL = 0
    HDFS = 1

    def is_hdfs(self):
        return self.value == self.HDFS

    def is_eggroll(self):
        return self.value == self.EGGROLL

class RetCode(IntEnum):
    SUCCESS = 0
    EXCEPTION_ERROR = 100
    PARAMETER_ERROR = 101
    DATA_ERROR = 102
    OPERATING_ERROR = 103
    FEDERATED_ERROR = 104
    CONNECTION_ERROR = 105
    SERVER_ERROR = 500


class FederatedSchedulingStatusCode(object):
    SUCCESS = 0
    PARTIAL = 1
    FAILED = 3


class BaseStatus(object):
    @classmethod
    def status_list(cls):
        return [k for k in cls.__dict__.keys() if not callable(getattr(cls, k)) and not k.startswith("__")]

    @classmethod
    def contains(cls, status):
        return status in cls.status_list()


class StatusSet(BaseStatus):
    WAITING = 'WAITING'
    START = 'START'
    RUNNING = "RUNNING"
    CANCELED = "CANCELED"
    TIMEOUT = "TIMEOUT"
    FAILED = "FAILED"
    COMPLETE = "COMPLETE"

    @classmethod
    def get_level(cls, status):
        return dict(zip(cls.status_list(), range(len(cls.status_list())))).get(status, None)


class JobStatus(BaseStatus):
    WAITING = StatusSet.WAITING
    RUNNING = StatusSet.RUNNING
    CANCELED = StatusSet.CANCELED
    TIMEOUT = StatusSet.TIMEOUT
    FAILED = StatusSet.FAILED
    COMPLETE = StatusSet.COMPLETE


class TaskSetStatus(BaseStatus):
    WAITING = StatusSet.WAITING
    RUNNING = StatusSet.RUNNING
    CANCELED = StatusSet.CANCELED
    TIMEOUT = StatusSet.TIMEOUT
    FAILED = StatusSet.FAILED
    COMPLETE = StatusSet.COMPLETE


class TaskStatus(BaseStatus):
    WAITING = StatusSet.WAITING
    START = StatusSet.START
    RUNNING = StatusSet.RUNNING
    CANCELED = StatusSet.CANCELED
    TIMEOUT = StatusSet.TIMEOUT
    FAILED = StatusSet.FAILED
    COMPLETE = StatusSet.COMPLETE


class OngoingStatus(BaseStatus):
    WAITING = StatusSet.WAITING
    START = StatusSet.START
    RUNNING = StatusSet.RUNNING


class InterruptStatus(BaseStatus):
    CANCELED = StatusSet.CANCELED
    TIMEOUT = StatusSet.TIMEOUT
    FAILED = StatusSet.FAILED


class EndStatus(BaseStatus):
    CANCELED = StatusSet.CANCELED
    TIMEOUT = StatusSet.TIMEOUT
    FAILED = StatusSet.FAILED
    COMPLETE = StatusSet.COMPLETE

    @staticmethod
    def is_end_status(status):
        return status in EndStatus.__dict__.keys()


class ModelStorage(object):
    REDIS = "redis"
    MYSQL = "mysql"


class ModelOperation(object):
    EXPORT = "export"
    IMPORT = "import"
    STORE = "store"
    RESTORE = "restore"
    LOAD = "load"
    BIND = "bind"


class ProcessRole(object):
    SERVER = "server"
    EXECUTOR = "executor"
