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


import abc
from typing import Iterable

import six

from arch.api.utils.core_utils import current_timestamp, serialize_b64, deserialize_b64
from fate_arch.common.log import getLogger
from fate_arch.db.db_models import DB, MachineLearningDataSchema

LOGGER = getLogger()


@six.add_metaclass(abc.ABCMeta)
class TableABC(object):
    """
    table for distributed storage
    """

    @abc.abstractmethod
    def get_partitions(self):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_namespace(self):
        pass

    @abc.abstractmethod
    def get_storage_engine(self):
        pass

    @abc.abstractmethod
    def get_address(self):
        pass

    @abc.abstractmethod
    def put_all(self, kv_list: Iterable, **kwargs):
        """
        Puts (key, value) 2-tuple stream from the iterable items.

        Elements must be exact 2-tuples, they may not be of any other type, or tuple subclass.
        Parameters
        ----------
        kv_list : Iterable
          Key-Value 2-tuple iterable. Will be serialized.
        Notes
        -----
        Each key must be less than 512 bytes, value must be less than 32 MB(implementation depends).
        """
        pass

    @abc.abstractmethod
    def collect(self, **kwargs) -> list:
        """
        Returns an iterator of (key, value) 2-tuple from the Table.

        Returns
        -------
        Iterator
        """
        pass

    @abc.abstractmethod
    def count(self):
        """
        Returns the number of elements in the Table.

        Returns
        -------
        int
          Number of elements in this Table.
        """
        pass

    @abc.abstractmethod
    def save_as(self, name, namespace, partition=None, schema_data=None, **kwargs):
        if schema_data:
            self.save_schema(name=name, namespace=namespace, schema_data=schema_data, partitions=partition)

    @abc.abstractmethod
    def close(self):
        pass

    def destroy(self):
        # destroy schema
        self.destroy_schema()
        # subclass method needs do: super().destroy()

    """
    meta utils
    """

    def get_schema(self, _type='schema', name=None, namespace=None):
        if not name and not namespace:
            name = self._name
            namespace = self._namespace
        with DB.connection_context():
            schema = MachineLearningDataSchema.select().where(MachineLearningDataSchema.f_table_name == name,
                                                              MachineLearningDataSchema.f_namespace == namespace)
            schema_data = {}
            if schema:
                schema = schema[0]
                try:
                    if _type == 'schema':
                        schema_data = deserialize_b64(schema.f_schema)
                    elif _type == 'data':
                        schema_data = deserialize_b64(schema.f_part_of_data)
                    elif _type == 'count':
                        schema_data = schema.f_count
                    elif _type == 'partitions':
                        schema_data = schema.f_partitions
                except:
                    schema_data = None
        return schema_data

    def save_schema(self, schema_data=None, name=None, namespace=None, party_of_data=None, count=0, partitions=1):
        # save metas to mysql
        if not schema_data:
            schema_data = {}
        if not party_of_data:
            party_of_data = []
        if not name or not namespace:
            name = self.get_name()
            namespace = self.get_namespace()
        with DB.connection_context():
            schema = MachineLearningDataSchema.select().where(MachineLearningDataSchema.f_table_name == name,
                                                              MachineLearningDataSchema.f_namespace == namespace)
            if schema:
                # save schema info
                schema = schema[0]
                if schema.f_schema:
                    _schema_data = deserialize_b64(schema.f_schema)
                _schema_data.update(schema_data)
                schema.f_schema = serialize_b64(_schema_data, to_str=True)
                # save data
                if party_of_data:
                    _f_part_of_data = deserialize_b64(schema.f_part_of_data)
                    if len(_f_part_of_data) < 100:
                        _f_part_of_data.extend(party_of_data[:(100 - len(_f_part_of_data))])
                        schema.f_part_of_data = serialize_b64(party_of_data[:100], to_str=True)
                # save count
                if count:
                    schema.f_count = count
                if partitions:
                    schema.f_partitions = partitions
            else:
                raise Exception('please create table {} {} before useing'.format(name, namespace))
            schema.f_update_time = current_timestamp()
            schema.save()

    def destroy_schema(self):
        try:
            with DB.connection_context():
                MachineLearningDataSchema \
                    .delete() \
                    .where(MachineLearningDataSchema.f_table_name == self.get_name(),
                           MachineLearningDataSchema.f_namespace == self.get_namespace()) \
                    .execute()
        except Exception as e:
            LOGGER.error("delete_table_meta {}, {}, exception:{}.".format(self.get_namespace(), self.get_name(), e))
