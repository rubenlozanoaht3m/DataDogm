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
import click
from fate_flow.utils.cli_utils import preprocess, access_server


@click.group(short_help="Queue Operations")
@click.pass_context
def queue(ctx):
    """Queue Operations"""
    pass


@queue.command(short_help="Clean Queue")
@click.pass_context
def clean(ctx, **kwargs):
    """
    - COMMAND DESCRIPTION:

    Queue Clean Command
    """
    # config_data, dsl_data = preprocess(**kwargs)
    # access_server('post', ctx, 'job/clean/queue', config_data)
    click.echo('Not Done Yet')
