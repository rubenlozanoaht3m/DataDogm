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


CONF_PATH = click.option("-c", "--conf-path", type=click.Path(exists=True), required=True,
                         help="Configuration file path.")

DSL_PATH = click.option("-d", "--dsl-path", type=click.Path(exists=True),
                        help="Domain-specific language(DSL) file path. If the type of job is 'predict', "
                             "you can leave this feature blank, or you can provide a valid dsl file to "
                             "replace the one that aotumatically generated by fate.")

LIMIT = click.option("-l", "--limit", type=click.INT, default=10,
                     help="LIMIT flag constrains the number of records to return. (default: 10)")

JOBID = click.option("-j", "--job-id", type=click.STRING,
                     help="A valid job id.")

JOBID_REQUIRED = click.option("-j", "--job-id", type=click.STRING, required=True,
                              help="A valid job id.")

role_choices_list = ["local", "guest", "arbiter", "host"]

ROLE = click.option("-r", "--role", type=click.Choice(role_choices_list), metavar="TEXT",
                    help="Role name. Users can choose one from {} and {}.".format(",".join(role_choices_list[:-1]),
                                                                                  role_choices_list[-1]))

ROLE_REQUIRED = click.option("-r", "--role", type=click.Choice(role_choices_list), required=True, metavar="TEXT",
                             help="Role name. Users can choose one from {} and {}.".format(",".join(role_choices_list[:-1]),
                                                                                           role_choices_list[-1]))

PARTYID = click.option("-p", "--party-id", type=click.STRING,
                       help="A valid party id.")

PARTYID_REQUIRED = click.option("-p", "--party-id", type=click.STRING, required=True,
                                help="A valid party id.")

COMPONENT_NAME = click.option("-cpn", "--component-name", type=click.STRING,
                              help="A valid component name.")

COMPONENT_NAME_REQUIRED = click.option("-cpn", "--component-name", type=click.STRING, required=True,
                                       help="A valid component name.")

status_choices_list = ["complete", "failed", "running", "waiting", "timeout", "canceled", "partial", "deleted"]

STATUS = click.option("-s", "--status", type=click.Choice(status_choices_list), metavar="TEXT",
                      help="Job status. Users can choose one from {} and {}.".format(", ".join(status_choices_list[:-1]),
                                                                                     status_choices_list[-1]))

OUTPUT_PATH_REQUIRED = click.option("-o", "--output-path", type=click.Path(exists=False), required=True,
                                    help="User specifies output directory path.")

OUTPUT_PATH = click.option("-o", "--output-path", type=click.Path(exists=False),
                           help="User specifies output directory path.")

NAMESPACE = click.option("-n", "--namespace", type=click.STRING,
                         help="Namespace.")

TABLE_NAME = click.option("-t", "--table-name", type=click.STRING,
                          help="Table name.")

NAMESPACE_REQUIRED = click.option("-n", "--namespace", type=click.STRING, required=True,
                                  help="Namespace.")

TABLE_NAME_REQUIRED = click.option("-t", "--table-name", type=click.STRING, required=True,
                                   help="Table name.")

TAG_NAME_REQUIRED = click.option("-t", "--tag-name", type=click.STRING, required=True,
                                 help="The name of tag.")

TAG_DESCRIPTION = click.option("-d", "--tag-desc", type=click.STRING,
                               help="The description of tag. Note that if there are some whitespaces in description, "
                               "please make sure the description text is enclosed in double quotation marks.")

MODEL_VERSION = click.option("-m", "--model-version", type=click.STRING,
                             help="Model version.")

MODEL_VERSION_REQUIRED = click.option("--model-version", type=click.STRING, required=True, help="Model version.")

MODEL_ID_REQUIRED = click.option("--model-id", type=click.STRING, required=True, help="Model id.")