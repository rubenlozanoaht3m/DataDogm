#
#  Copyright 2019 The Eggroll Authors. All Rights Reserved.
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

import itertools

from fate_arch.abc import AddressABC, CTableABC
from fate_arch.common.profile import computing_profile
from fate_arch.standalone import Table as RawTable


class Table(CTableABC):
    def __init__(self, table: RawTable):
        self._table = table

    def __getstate__(self):
        pass

    def as_federation_format(self):
        return self._table

    @property
    def partitions(self):
        return self._table.partitions

    @computing_profile
    def save(self, address: AddressABC, partitions: int, schema: dict, **kwargs):
        from fate_arch.common.address import StandaloneAddress
        if isinstance(address, StandaloneAddress):
            self._table.save_as(name=address.name, namespace=address.namespace, partition=partitions,
                                need_cleanup=False)
            schema.update(self.schema)
            return
        raise NotImplementedError(f"address type {type(address)} not supported with standalone backend")

    @computing_profile
    def count(self) -> int:
        return self._table.count()

    @computing_profile
    def collect(self, **kwargs):
        return self._table.collect(**kwargs)

    @computing_profile
    def take(self, n=1, **kwargs):
        if n <= 0:
            raise ValueError(f"{n} <= 0")
        return list(itertools.islice(self.collect(), n))

    @computing_profile
    def first(self, **kwargs):
        resp = self.take(1, **kwargs)
        if len(resp) < 1:
            raise RuntimeError(f"table is empty")
        return resp[0]

    @computing_profile
    def reduce(self, func, key_func=None, **kwargs):
        if key_func is None:
            return self._table.reduce(func)

        it = self._table.collect()
        ret = {}
        for k, v in it:
            agg_key = key_func(k)
            if agg_key in ret:
                ret[agg_key] = func(ret[agg_key], v)
            else:
                ret[agg_key] = v
        return ret

    @computing_profile
    def map(self, func):
        return Table(self._table.map(func))

    @computing_profile
    def mapValues(self, func):
        return Table(self._table.mapValues(func))

    @computing_profile
    def flatMap(self, func):
        return Table(self._table.flatMap(func))

    @computing_profile
    def mapPartitions(self, func):
        return Table(self._table.mapPartitions(func))

    @computing_profile
    def mapPartitions2(self, func):
        return Table(self._table.mapPartitions2(func))

    @computing_profile
    def glom(self):
        return Table(self._table.glom())

    @computing_profile
    def sample(self, fraction, seed=None):
        return Table(self._table.sample(fraction, seed))

    @computing_profile
    def filter(self, func):
        return Table(self._table.filter(func))

    @computing_profile
    def join(self, other: 'Table', func):
        return Table(self._table.join(other._table, func))

    @computing_profile
    def subtractByKey(self, other: 'Table'):
        return Table(self._table.subtractByKey(other._table))

    @computing_profile
    def union(self, other: 'Table', func=lambda v1, v2: v1):
        return Table(self._table.union(other._table, func))
