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
import os
import json
import time
import click
import requests
from contextlib import closing

from fate_flow.utils import detect_utils, cli_args
from fate_flow.utils.cli_utils import (preprocess, download_from_request,
                                       access_server, prettify)


@click.group(short_help="Job Operations")
@click.pass_context
def job(ctx):
    """
    \b
    Provides numbers of job operational commands, including submit, stop, query and etc.
    For more details, please check out the help text.
    """
    pass


@job.command("submit", short_help="Submit Job Command")
@cli_args.CONF_PATH
@cli_args.DSL_PATH
@click.pass_context
def submit(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Submit a pipeline job.
    Used to be 'submit_job'.

    \b
    - USAGE:
        flow job submit -c fate_flow/examples/test_hetero_lr_job_conf.json -d fate_flow/examples/test_hetero_lr_job_dsl.json
    """
    config_data, dsl_data = preprocess(**kwargs)
    post_data = {
        'job_dsl': dsl_data,
        'job_runtime_conf': config_data
    }

    response = access_server('post', ctx, 'job/submit', post_data, False)

    try:
        if response.json()['retcode'] == 999:
            click.echo('use service.sh to start standalone node server....')
            os.system('sh service.sh start --standalone_node')
            time.sleep(5)
            access_server('post', ctx, 'job/submit', post_data)
        else:
            prettify(response.json())
    except:
        pass


@job.command("list", short_help="List Job Command")
@cli_args.LIMIT
@click.pass_context
def list(ctx, **kwargs):
    """
    - DESCRIPTION:

    List job.

    \b
    - USAGE:
        flow job list
        flow job list -l 30
    """
    config_data, dsl_data = preprocess(**kwargs)
    access_server('post', ctx, 'job/list/job', config_data)


@job.command("query", short_help="Query Job Command")
@cli_args.JOBID
@cli_args.ROLE
@cli_args.PARTYID
@cli_args.COMPONENT_NAME
@cli_args.STATUS
@click.pass_context
def query(ctx, **kwargs):
    """
    \b
    - DESCRIPTION:
        Query job information by filters.
        Used to be 'query_job'.

    \b
    - USAGE:
        flow job query -r guest -p 9999 -s success
        flow job query -j $JOB_ID -cpn hetero_feature_binning_0
    """
    config_data, dsl_data = preprocess(**kwargs)
    response = access_server('post', ctx, "job/query", config_data, False)
    if isinstance(response, requests.models.Response):
        response = response.json()
    if response['retcode'] == 0:
        for i in range(len(response['data'])):
            del response['data'][i]['f_runtime_conf']
            del response['data'][i]['f_dsl']
    prettify(response.json() if isinstance(response, requests.models.Response) else response)


@job.command("clean", short_help="Clean Job Command")
@cli_args.JOBID
@cli_args.ROLE
@cli_args.PARTYID
@cli_args.COMPONENT_NAME
@click.pass_context
def clean(ctx, **kwargs):
    """
    \b
    - DESCRIPTION:
        Clean processor, data table and metric data.
        Used to be 'clean_job'.

    \b
    - USAGE:
        flow job clean -r guest -p 9999
        flow job clean -j $JOB_ID -cpn hetero_feature_binning_0
    """
    config_data, dsl_data = preprocess(**kwargs)
    detect_utils.check_config(config=config_data, required_arguments=['job_id'])
    access_server('post', ctx, "job/clean", config_data)


@job.command("stop", short_help="Stop Job Command")
@cli_args.JOBID_REQUIRED
@click.pass_context
def stop(ctx, **kwargs):
    """
    \b
    - DESCRIPTION:
        Stop a specified job.

    \b
    - USAGE:
        flow job stop -j $JOB_ID
    """
    config_data, dsl_data = preprocess(**kwargs)
    detect_utils.check_config(config=config_data, required_arguments=['job_id'])
    access_server('post', ctx, "job/stop", config_data)


@job.command("config", short_help="Config Job Command")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.OUTPUT_PATH
@click.pass_context
def config(ctx, **kwargs):
    """
    \b
    - DESCRIPTION:
        Download Configurations of A Specified Job.

    \b
    - USAGE:
        flow job config -j $JOB_ID -r host -p 10000 --output-path ./examples/
    """
    config_data, dsl_data = preprocess(**kwargs)
    detect_utils.check_config(config=config_data, required_arguments=['job_id', 'role', 'party_id', 'output_path'])
    response = access_server('post', ctx, 'job/config', config_data, False).json()
    if response['retcode'] == 0:
        job_id = response['data']['job_id']
        download_directory = os.path.join(config_data['output_path'], 'job_{}_config'.format(job_id))
        os.makedirs(download_directory, exist_ok=True)
        for k, v in response['data'].items():
            if k == 'job_id':
                continue
            with open('{}/{}.json'.format(download_directory, k), 'w') as fw:
                json.dump(v, fw, indent=4)
        del response['data']['dsl']
        del response['data']['runtime_conf']
        response['directory'] = download_directory
        response['retmsg'] = 'download successfully, please check {} directory'.format(download_directory)
    prettify(response.json() if isinstance(response, requests.models.Response) else response)


@job.command("log", short_help="Log Job Command")
@cli_args.JOBID_REQUIRED
@cli_args.OUTPUT_PATH
@click.pass_context
def log(ctx, **kwargs):
    """
    \b
    - DESCRIPTION:
        Download Log Files of A Specified Job.

    \b
    - USAGE:
        flow job log -j JOB_ID --output-path ./examples/
    """
    config_data, dsl_data = preprocess(**kwargs)
    detect_utils.check_config(config=config_data, required_arguments=['job_id', 'output_path'])
    job_id = config_data['job_id']
    tar_file_name = 'job_{}_log.tar.gz'.format(job_id)
    extract_dir = os.path.join(config_data['output_path'], 'job_{}_log'.format(job_id))
    with closing(access_server('get', ctx, 'job/log', config_data, False, stream=True)) as response:
        if response.status_code == 200:
            download_from_request(http_response=response, tar_file_name=tar_file_name, extract_dir=extract_dir)
            response = {'retcode': 0,
                        'directory': extract_dir,
                        'retmsg': 'download successfully, please check {} directory'.format(extract_dir)}
        else:
            response = response.json()
    prettify(response.json() if isinstance(response, requests.models.Response) else response)


@job.command("view", short_help="Query Job Data View Command")
@cli_args.JOBID
@cli_args.ROLE
@cli_args.PARTYID
@cli_args.COMPONENT_NAME
@cli_args.STATUS
@click.pass_context
def view(ctx, **kwargs):
    """
    \b
    - DESCRIPTION:
        Query job data view information by filters.
        Used to be 'data_view_query'.

    \b
    - USAGE:
        flow job view -r guest -p 9999
        flow job view -j $JOB_ID -cpn hetero_feature_binning_0
    """
    config_data, dsl_data = preprocess(**kwargs)
    access_server('post', ctx, 'job/data/view/query', config_data)


@job.command("dsl", short_help="Generate Predict DSL Command")
@click.option("--cpn-list", type=click.STRING,
              help="User inputs a string to specify component list")
@click.option("--cpn-path", type=click.Path(exists=True),
              help="User specify a file path which records the component list.")
@click.option("--train-dsl-path", type=click.Path(exists=True), required=True,
              help="User specifies the train dsl file path.")
@cli_args.OUTPUT_PATH
@click.pass_context
def dsl_generator(ctx, **kwargs):
    """
    \b
    - DESCRIPTION:
        A predict dsl generator.
        Before using predict dsl generator, users should prepare:
            1. name list of component which you are going to use in predict progress,
            2. the train dsl file path you specified in train progress.
        \b
        Notice that users can choose to specify the component name list by using a text file,
        or, by typing in terminal. We, however, strongly recommend users using prepared files
        to specify the component list in order to avoid some unnecessary mistakes.

    \b
    - USAGE:
        flow job dsl --cpn-path fate_flow/examples/component_list.txt --train-dsl-path fate_flow/examples/test_hetero_lr_job_dsl.json -o fate_flow/examples/generated_predict_dsl.json
        flow job dsl --cpn-list "dataio_0, hetero_feature_binning_0, hetero_feature_selection_0, evaluation_0" --train-dsl-path fate_flow/examples/test_hetero_lr_job_dsl.json -o fate_flow/examples/generated_predict_dsl.json
        flow job dsl --cpn-list [dataio_0,hetero_feature_binning_0,hetero_feature_selection_0,evaluation_0] --train-dsl-path fate_flow/examples/test_hetero_lr_job_dsl.json -o fate_flow/examples/generated_predict_dsl.json
    """
    if kwargs.get("cpn_list"):
        cpn_str = kwargs.get("cpn_list")
    elif kwargs.get("cpn_path"):
        with open(kwargs.get("cpn_path"), "r") as fp:
            cpn_str = fp.read()
    else:
        cpn_str = ""

    with open(kwargs.get("train_dsl_path"), "r") as ft:
        train_dsl = ft.read()

    output_path = kwargs.get("output_path")
    if not os.path.isabs(output_path):
        output_path = os.path.join(os.path.abspath(os.curdir), output_path)

    config_data = {
        "cpn_str": cpn_str,
        "train_dsl": train_dsl,
        "output_path": output_path
    }

    access_server('post', ctx, 'job/dsl/generate', config_data)
