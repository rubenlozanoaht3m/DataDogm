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
from typing import Iterable
from arch.api.utils.core import json_dumps, json_loads
from arch.api.utils import version_control
from arch.api import eggroll
import datetime
import warnings

warnings.warn("the storage module is deprecated, use apis from Table/TableManager directly", DeprecationWarning,
              stacklevel=2)


def init_storage(work_mode, backend=0, job_id=None):
    eggroll.init(job_id=job_id, mode=work_mode, backend=backend)


def table(name: str, namespace: str, partition: int = 1, persistent: bool = True, create_if_missing: bool = True,
          error_if_exist: bool = False,
          in_place_computing: bool = False):
    data_table = eggroll.table(name=name, namespace=namespace, partition=partition, persistent=persistent,
                               create_if_missing=create_if_missing, error_if_exist=error_if_exist,
                               in_place_computing=in_place_computing)
    return data_table


def save_data(kv_data: Iterable, name, namespace, partition=1, persistent: bool = True, create_if_missing=True, error_if_exist=False,
              in_version: bool = False, version_log=None):
    """
    save data into data table
    :param kv_data:
    :param name: table name of data table
    :param namespace: table namespace of data table
    :param partition: number of partition
    :param create_if_missing:
    :param error_if_exist:
    :return:
        data table instance
    """
    data_table = eggroll.table(name=name, namespace=namespace, partition=partition, persistent=persistent,
                               create_if_missing=create_if_missing, error_if_exist=error_if_exist)
    data_table.put_all(kv_data)
    if in_version:
        version_log = "[AUTO] save data at %s." % datetime.datetime.now() if not version_log else version_log
        version_control.save_version(name=name, namespace=namespace, version_log=version_log)
    return data_table


def get_data_table(name, namespace):
    """
    return data table instance by table name and table name space
    :param name: table name of data table
    :param namespace: table name space of data table
    :return:
        data table instance
    """
    return eggroll.table(name=name, namespace=namespace, create_if_missing=False)


def save_data_table_meta(kv, data_table_name, data_table_namespace):
    """
    save data table meta information
    :param kv: v should be serialized by JSON
    :param data_table_name: table name of this data table
    :param data_table_namespace: table name of this data table
    :return:
    """
    data_meta_table = eggroll.table(name="%s.meta" % data_table_name,
                                    namespace=data_table_namespace,
                                    partition=1,
                                    create_if_missing=True, error_if_exist=False)
    for k, v in kv.items():
        data_meta_table.put(k, json_dumps(v), use_serialize=False)


def get_data_table_meta_by_instance(key, data_table):
    return get_data_table_meta(key, data_table._name, data_table._namespace)


def get_data_table_meta(key, data_table_name, data_table_namespace):
    """
    get data table meta information
    :param key:
    :param data_table_name: table name of this data table
    :param data_table_namespace: table name of this data table
    :return:
    """
    data_meta_table = eggroll.table(name="%s.meta" % data_table_name,
                                    namespace=data_table_namespace,
                                    create_if_missing=True,
                                    error_if_exist=False)
    if data_meta_table:
        value_bytes = data_meta_table.get(key, use_serialize=False)
        if value_bytes:
            return json_loads(value_bytes)
        else:
            return None
    else:
        return None


def get_data_table_metas_by_instance(data_table):
    return get_data_table_metas(data_table._name, data_table._namespace)


def get_data_table_metas(data_table_name, data_table_namespace):
    """
    get data table meta information
    :param data_table_name: table name of this data table
    :param data_table_namespace: table name of this data table
    :return:
    """
    data_meta_table = eggroll.table(name="%s.meta" % data_table_name,
                                    namespace=data_table_namespace,
                                    create_if_missing=True,
                                    error_if_exist=False)
    if data_meta_table:
        metas = dict()
        for k, v in data_meta_table.collect(use_serialize=False):
            metas[k] = json_loads(v)
        return metas
    else:
        return None


def clean_table(namespace, regex_string='*'):
    try:
        eggroll.cleanup(regex_string, namespace=namespace, persistent=False)
    except Exception as e:
        print(e)
