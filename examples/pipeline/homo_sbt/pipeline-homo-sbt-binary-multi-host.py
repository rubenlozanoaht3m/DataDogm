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

import argparse

from pipeline.backend.pipeline import PipeLine
from pipeline.component.data_transform import DataTransform
from pipeline.component.homo_secureboost import HomoSecureBoost
from pipeline.component.reader import Reader
from pipeline.interface.data import Data
from pipeline.component.evaluation import Evaluation
from pipeline.interface.model import Model

from pipeline.utils.tools import load_job_config
from pipeline.runtime.entity import JobParameters


def main(config="../../config.yaml", namespace=""):

    # obtain config
    if isinstance(config, str):
        config = load_job_config(config)

    parties = config.parties
    guest = parties.guest[0]
    host_0 = parties.host[0]
    host_1 = parties.host[1]
    arbiter = parties.arbiter[0]

    backend = config.backend
    work_mode = config.work_mode

    guest_train_data = {"name": "default_credit_guest", "namespace": f"experiment{namespace}"}
    host_train_data_0 = {"name": "default_credit_host1", "namespace": f"experiment{namespace}"}
    host_train_data_1 = {"name": "default_credit_host2", "namespace": f"experiment{namespace}"}

    guest_validate_data = {"name": "default_credit_test", "namespace": f"experiment{namespace}"}
    host_validate_data_0 = {"name": "default_credit_test", "namespace": f"experiment{namespace}"}
    host_validate_data_1 = {"name": "default_credit_test", "namespace": f"experiment{namespace}"}

    pipeline = PipeLine().set_initiator(role='guest', party_id=guest).set_roles(guest=guest, host=[host_0, host_1]
                                                                                , arbiter=arbiter)

    data_transform_0, data_transform_1 = DataTransform(name="data_transform_0"), DataTransform(name='data_transform_1')
    reader_0, reader_1 = Reader(name="reader_0"), Reader(name='reader_1')

    reader_0.get_party_instance(role='guest', party_id=guest).component_param(table=guest_train_data)
    reader_0.get_party_instance(role='host', party_id=host_0).component_param(table=host_train_data_0)
    reader_0.get_party_instance(role='host', party_id=host_1).component_param(table=host_train_data_1)

    data_transform_0.get_party_instance(role='guest', party_id=guest).component_param(with_label=True, output_format="dense")
    data_transform_0.get_party_instance(role='host', party_id=host_0).component_param(with_label=True, output_format="dense")
    data_transform_0.get_party_instance(role='host', party_id=host_1).component_param(with_label=True, output_format="dense")

    reader_1.get_party_instance(role='guest', party_id=guest).component_param(table=guest_validate_data)
    reader_1.get_party_instance(role='host', party_id=host_0).component_param(table=host_validate_data_0)
    reader_1.get_party_instance(role='host', party_id=host_1).component_param(table=host_validate_data_1)
    data_transform_1.get_party_instance(role='guest', party_id=guest).component_param(with_label=True, output_format="dense")
    data_transform_1.get_party_instance(role='host', party_id=host_0).component_param(with_label=True, output_format="dense")
    data_transform_1.get_party_instance(role='host', party_id=host_1).component_param(with_label=True, output_format="dense")

    homo_secureboost_0 = HomoSecureBoost(name="homo_secureboost_0",
                                         num_trees=3,
                                         task_type='classification',
                                         objective_param={"objective": "cross_entropy"},
                                         tree_param={
                                             "max_depth": 3
                                         },
                                         validation_freqs=1
                                         )

    evaluation_0 = Evaluation(name='evaluation_0', eval_type='binary')

    pipeline.add_component(reader_0)
    pipeline.add_component(data_transform_0, data=Data(data=reader_0.output.data))
    pipeline.add_component(reader_1)
    pipeline.add_component(data_transform_1, data=Data(data=reader_1.output.data), model=Model(data_transform_0.output.model))
    pipeline.add_component(homo_secureboost_0, data=Data(train_data=data_transform_0.output.data,
                                                         validate_data=data_transform_1.output.data
                                                         ))
    pipeline.add_component(evaluation_0, data=Data(homo_secureboost_0.output.data))

    pipeline.compile()
    job_parameters = JobParameters(backend=backend, work_mode=work_mode)
    pipeline.fit(job_parameters)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("PIPELINE DEMO")
    parser.add_argument("-config", type=str,
                        help="config file")
    args = parser.parse_args()
    if args.config is not None:
        main(args.config)
    else:
        main()
