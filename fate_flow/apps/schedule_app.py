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

from flask import Flask, request

from fate_flow.entity.constant import RetCode
from fate_flow.operation.job_controller import JobController
from fate_flow.operation.job_saver import JobSaver
from fate_flow.settings import stat_logger
from fate_flow.utils.api_utils import get_json_result
from fate_flow.utils.authentication_utils import request_authority_certification
from fate_flow.utils import job_utils

manager = Flask(__name__)


@manager.errorhandler(500)
def internal_server_error(e):
    stat_logger.exception(e)
    return get_json_result(retcode=RetCode.EXCEPTION_ERROR, retmsg=str(e))


@manager.route('/<job_id>/<role>/<party_id>/create', methods=['POST'])
@request_authority_certification
def create_job(job_id, role, party_id):
    JobController.create_job(job_id=job_id, role=role, party_id=int(party_id), job_info=request.json)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<role>/<party_id>/initialize', methods=['POST'])
@request_authority_certification
def initialize_job(job_id, role, party_id):
    JobController.initialize_job(job_id=job_id, role=role, party_id=int(party_id))
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<role>/<party_id>/check', methods=['POST'])
def check_job(job_id, role, party_id):
    status = JobController.check_job_run(job_id, role, party_id)
    if status:
        return get_json_result(retcode=0, retmsg='success')
    else:
        return get_json_result(retcode=101, retmsg='The job running on the host side exceeds the maximum running amount')


@manager.route('/<job_id>/<role>/<party_id>/start', methods=['POST'])
def start_job(job_id, role, party_id):
    JobController.start_job(job_id=job_id, role=role, party_id=int(party_id))
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<role>/<party_id>/model', methods=['POST'])
@request_authority_certification
def save_pipeline(job_id, role, party_id):
    JobController.save_pipeline(job_id=job_id, role=role, party_id=party_id)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<role>/<party_id>/stop/<stop_status>', methods=['POST'])
def stop_job(job_id, role, party_id, stop_status):
    JobController.stop_job(job_id=job_id, role=role, party_id=int(party_id), stop_status=stop_status)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<role>/<party_id>/cancel', methods=['POST'])
def cancel_job(job_id, role, party_id):
    res = JobController.cancel_job(job_id=job_id, role=role, party_id=int(party_id),
                                   job_initiator=request.json.get('job_initiator', {}))
    if res:
        return get_json_result(retcode=0, retmsg='cancel job success')
    return get_json_result(retcode=101, retmsg='cancel job failed')


@manager.route('/<job_id>/<role>/<party_id>/<roles>/<party_ids>/clean', methods=['POST'])
@request_authority_certification
def clean(job_id, role, party_id, roles, party_ids):
    JobController.clean_job(job_id=job_id, role=role, party_id=party_id, roles=roles, party_ids=party_ids)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<task_set_id>/<role>/<party_id>/stop/<stop_status>', methods=['POST'])
def stop_task_set(job_id, task_set_id, role, party_id, stop_status):
    for task_set in JobSaver.query_task_set(job_id=job_id, task_set_id=task_set_id, role=role, party_id=party_id):
        JobController.stop_task_set(task_set=task_set, stop_status=stop_status)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<component_name>/<task_id>/<task_version>/<role>/<party_id>/start', methods=['POST'])
@request_authority_certification
def start_task(job_id, component_name, task_id, task_version, role, party_id):
    JobController.start_task(job_id, component_name, task_id, task_version, role, party_id, request.json)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<component_name>/<task_id>/<task_version>/<role>/<party_id>/update', methods=['POST'])
def update_task(job_id, component_name, task_id, task_version, role, party_id):
    task_info = {
        "task_id": task_id,
        "task_version": task_version,
        "role": role,
        "party_id": party_id,
    }
    task_info.update(request.json)
    JobController.update_task(task_info=task_info)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<component_name>/<task_id>/<task_version>/<role>/<party_id>/stop/<stop_status>', methods=['POST'])
def stop_task(job_id, component_name, task_id, task_version, role, party_id, stop_status):
    tasks = job_utils.query_task(job_id=job_id, task_id=task_id, task_version=task_version, role=role, party_id=int(party_id))
    for task in tasks:
        JobController.stop_task(task=task, stop_status=stop_status)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<component_name>/<task_id>/<task_version>/<role>/<party_id>/input/args', methods=['POST'])
def query_task_input_args(job_id, component_name, task_id, task_version, role, party_id):
    task_input_args = JobController.query_task_input_args(job_id, task_id, role, party_id,
                                                          job_args=request.json.get('job_args', {}),
                                                          job_parameters=request.json.get('job_parameters', {}),
                                                          input_dsl=request.json.get('input', {}),
                                                          filter_type=['data'],
                                                          filter_attr={'data': ['partitions']})
    return get_json_result(retcode=0, retmsg='success', data=task_input_args)
