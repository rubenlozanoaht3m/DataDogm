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
import threading
import time
import sys

from fate_flow.utils.authentication_utils import authentication_check
from federatedml.protobuf.generated import pipeline_pb2
from arch.api.utils.log_utils import schedule_logger
from fate_flow.db.db_models import Task
from fate_flow.operation.task_executor import TaskExecutor
from fate_flow.scheduler.task_scheduler import TaskScheduler
from fate_flow.scheduler.federated_scheduler import FederatedScheduler
from fate_flow.entity.constant import JobStatus, TaskSetStatus, TaskStatus
from fate_flow.entity.runtime_config import RuntimeConfig
from fate_flow.operation.job_tracker import Tracker
from fate_flow.settings import USE_AUTHENTICATION
from fate_flow.utils import job_utils, job_controller_utils
from fate_flow.utils.job_utils import save_job_conf, get_job_dsl_parser
import os
from fate_flow.operation.job_saver import JobSaver
from arch.api.utils.core_utils import json_dumps, current_timestamp
from fate_flow.entity.constant import Backend
from fate_flow.controller.task_set_controller import TaskSetController


class JobController(object):
    @classmethod
    def create_job(cls, job_id, role, party_id, job_info, init_tracker=True):
        # parse job configuration
        dsl = job_info['dsl']
        runtime_conf = job_info['runtime_conf']
        train_runtime_conf = job_info['train_runtime_conf']
        if USE_AUTHENTICATION:
            authentication_check(src_role=job_info.get('src_role', None), src_party_id=job_info.get('src_party_id', None),
                                 dsl=dsl, runtime_conf=runtime_conf, role=role, party_id=party_id)
        save_job_conf(job_id=job_id,
                      job_dsl=dsl,
                      job_runtime_conf=runtime_conf,
                      train_runtime_conf=train_runtime_conf,
                      pipeline_dsl=None)
        job_parameters = runtime_conf['job_parameters']
        job_initiator = runtime_conf['initiator']

        # save new job into db
        if role == job_initiator['role'] and party_id == job_initiator['party_id']:
            is_initiator = 1
        else:
            is_initiator = 0
        job_info["status"] = JobStatus.WAITING
        roles = job_info['roles']
        # this party configuration
        job_info["role"] = role
        job_info["party_id"] = party_id
        job_info["is_initiator"] = is_initiator
        job_info["progress"] = 0
        JobSaver.create_job(job_info=job_info)

        dsl_parser = get_job_dsl_parser(dsl=dsl,
                                        runtime_conf=runtime_conf,
                                        train_runtime_conf=train_runtime_conf)
        cls.initialize_job(job_id=job_id, role=role, party_id=party_id, initiator_role=job_initiator['role'], initiator_party_id=job_initiator['party_id'], dsl_parser=dsl_parser)
        if init_tracker:
            cls.initialize_job_tracker(job_id=job_id, role=role, party_id=party_id, job_info=job_info, is_initiator=is_initiator, dsl_parser=dsl_parser)

    @classmethod
    def initialize_job_tracker(cls, job_id, role, party_id, job_info, is_initiator, dsl_parser):
        job_parameters = job_info['runtime_conf']['job_parameters']
        roles = job_info['roles']
        tracker = Tracker(job_id=job_id, role=role, party_id=party_id,
                          model_id=job_parameters["model_id"],
                          model_version=job_parameters["model_version"])
        if job_parameters.get("job_type", "") != "predict":
            tracker.init_pipelined_model()
        partner = {}
        show_role = {}
        for _role, _role_party in roles.items():
            if is_initiator or _role == role:
                show_role[_role] = show_role.get(_role, [])
                for _party_id in _role_party:
                    if is_initiator or _party_id == party_id:
                        show_role[_role].append(_party_id)

            if _role != role:
                partner[_role] = partner.get(_role, [])
                partner[_role].extend(_role_party)
            else:
                for _party_id in _role_party:
                    if _party_id != party_id:
                        partner[_role] = partner.get(_role, [])
                        partner[_role].append(_party_id)

        job_args = dsl_parser.get_args_input()
        dataset = {}
        dsl_version = 1
        if job_args.get('dsl_version'):
            if job_args.get('dsl_version') == 2:
                dsl_version = 2
            job_args.pop('dsl_version')
        for _role, _role_party_args in job_args.items():
            if is_initiator or _role == role:
                for _party_index in range(len(_role_party_args)):
                    _party_id = roles[_role][_party_index]
                    if is_initiator or _party_id == party_id:
                        dataset[_role] = dataset.get(_role, {})
                        dataset[_role][_party_id] = dataset[_role].get(_party_id, {})
                        if dsl_version == 1:
                            for _data_type, _data_location in _role_party_args[_party_index]['args']['data'].items():
                                dataset[_role][_party_id][_data_type] = '{}.{}'.format(_data_location['namespace'],
                                                                                       _data_location['name'])
                        else:
                            for key in _role_party_args[_party_index].keys():
                                for _data_type, _data_location in _role_party_args[_party_index][key].items():
                                    dataset[_role][_party_id][key] = '{}.{}'.format(
                                        _data_location['namespace'], _data_location['name'])
        tracker.log_job_view({'partner': partner, 'dataset': dataset, 'roles': show_role})

    @classmethod
    def initialize_job(cls, job_id, role, party_id, initiator_role, initiator_party_id, dsl_parser):
        """
        Parse the DAG and create TaskSet/Task
        :param job_id:
        :param role:
        :param party_id:
        :param initiator_role:
        :param initiator_party_id:
        :param dsl_parser:
        :return:
        """
        component_map, task_sets = dsl_parser.get_dsl_hierarchical_structure()
        for i in range(len(task_sets)):
            task_set_info = {}
            task_set_info["job_id"] = job_id
            task_set_info["task_set_id"] = i
            task_set_info["initiator_role"] = initiator_role
            task_set_info["initiator_party_id"] = initiator_party_id
            task_set_info["role"] = role
            task_set_info["party_id"] = party_id
            task_set_info["status"] = TaskSetStatus.WAITING
            for component_name in task_sets[i]:
                component = dsl_parser.get_component_info(component_name=component_name)
                component_parameters = component.get_role_parameters()
                for parameters_on_party in component_parameters.get(role, []):
                    if parameters_on_party.get('local', {}).get('party_id') == party_id:
                        task_info = {}
                        task_info.update(task_set_info)
                        task_info["component_name"] = component_name
                        task_info["task_version"] = 0
                        task_info["task_id"] = job_utils.generate_task_id(job_id=job_id, component_name=component_name)
                        task_info["initiator_role"] = initiator_role
                        task_info["initiator_party_id"] = initiator_party_id
                        task_info["status"] = TaskStatus.WAITING
                        task_info["party_status"] = TaskStatus.WAITING
                        JobSaver.create_task(task_info=task_info)
            JobSaver.create_task_set(task_set_info=task_set_info)

    @classmethod
    def start_job(cls, job_id, role, party_id):
        job_info = {
            "job_id": job_id,
            "role": role,
            "party_id": party_id,
            "status": JobStatus.RUNNING,
            "party_status": JobStatus.RUNNING,
            "start_time": current_timestamp()
        }
        JobSaver.update_job(job_info=job_info)

    @classmethod
    def update_job(cls, job_info):
        """
        Save to local database
        :param job_info:
        :return:
        """
        JobSaver.update_job(job_info=job_info)

    @classmethod
    def stop_job(cls, job, stop_status):
        task_sets = JobSaver.query_task_set(job_id=job.f_job_id, role=job.f_role, party_id=job.f_party_id)
        for task_set in task_sets:
            TaskSetController.stop_task_set(task_set=task_set, stop_status=stop_status)
        # Job status depends on the final operation result and initiator calculate

    @classmethod
    def save_pipelined_model(cls, job_id, role, party_id):
        schedule_logger(job_id).info('job {} on {} {} start to save pipeline'.format(job_id, role, party_id))
        job_dsl, job_runtime_conf, train_runtime_conf = job_utils.get_job_configuration(job_id=job_id, role=role,
                                                                                        party_id=party_id)
        job_parameters = job_runtime_conf.get('job_parameters', {})
        model_id = job_parameters['model_id']
        model_version = job_parameters['model_version']
        job_type = job_parameters.get('job_type', '')
        if job_type == 'predict':
            return
        dag = job_utils.get_job_dsl_parser(dsl=job_dsl,
                                           runtime_conf=job_runtime_conf,
                                           train_runtime_conf=train_runtime_conf)
        predict_dsl = dag.get_predict_dsl(role=role)
        pipeline = pipeline_pb2.Pipeline()
        pipeline.inference_dsl = json_dumps(predict_dsl, byte=True)
        pipeline.train_dsl = json_dumps(job_dsl, byte=True)
        pipeline.train_runtime_conf = json_dumps(job_runtime_conf, byte=True)
        pipeline.fate_version = RuntimeConfig.get_env("FATE")
        pipeline.model_id = model_id
        pipeline.model_version = model_version
        tracker = Tracker(job_id=job_id, role=role, party_id=party_id, model_id=model_id, model_version=model_version)
        tracker.save_pipelined_model(pipelined_buffer_object=pipeline)
        schedule_logger(job_id).info('job {} on {} {} save pipeline successfully'.format(job_id, role, party_id))

    @classmethod
    def clean_job(cls, job_id, role, party_id, roles):
        schedule_logger(job_id).info('Job {} on {} {} start to clean'.format(job_id, role, party_id))
        tasks = job_utils.query_task(job_id=job_id, role=role, party_id=party_id)
        for task in tasks:
            try:
                Tracker(job_id=job_id, role=role, party_id=party_id, task_id=task.f_task_id, task_version=task.f_task_version).clean_task(roles)
                schedule_logger(job_id).info(
                    'Job {} component {} on {} {} clean done'.format(job_id, task.f_component_name, role, party_id))
            except Exception as e:
                schedule_logger(job_id).info(
                    'Job {} component {} on {} {} clean failed'.format(job_id, task.f_component_name, role, party_id))
                schedule_logger(job_id).exception(e)
        schedule_logger(job_id).info('job {} on {} {} clean done'.format(job_id, role, party_id))

    @classmethod
    def check_job_run(cls, job_id, role, party_id):
        return job_controller_utils.job_quantity_constraint(job_id, role, party_id)

    @classmethod
    def cancel_job(cls, job_id, role, party_id):
        schedule_logger(job_id).info('{} {} get cancel waiting job {} command'.format(role, party_id, job_id))
        jobs = job_utils.query_job(job_id=job_id)
        if jobs:
            job = jobs[0]
            job_runtime_conf = job.f_runtime_conf
            event = job_utils.job_event(job.f_job_id,
                                        job_runtime_conf['initiator']['role'],
                                        job_runtime_conf['initiator']['party_id'])
            try:
                RuntimeConfig.JOB_QUEUE.del_event(event)
            except:
                return False
            schedule_logger(job_id).info('cancel waiting job successfully, job id is {}'.format(job.f_job_id))
            return True
        else:
            raise Exception('role {} party id {} cancel waiting job failed, no find jod {}'.format(role, party_id, job_id))


class JobClean(threading.Thread):
    def run(self):
        time.sleep(5)
        jobs = job_utils.query_job(status=JobStatus.RUNNING, is_initiator=1)
        job_ids = set([job.f_job_id for job in jobs])
        for job_id in job_ids:
            schedule_logger(job_id).info('fate flow server start clean job')
            TaskScheduler.stop(job_id, JobStatus.FAILED)





