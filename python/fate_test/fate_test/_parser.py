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

import json
import typing
from collections import deque
from pathlib import Path

from fate_test import _config
import click
import prettytable

from fate_test._config import Parties, Config


# noinspection PyPep8Naming
class chain_hook(object):
    def __init__(self):
        self._hooks = []

    def add_hook(self, hook):
        self._hooks.append(hook)
        return self

    def add_extend_namespace_hook(self, namespace):
        self.add_hook(_namespace_hook(namespace))
        return self

    def add_replace_hook(self, mapping):
        self.add_hook(_replace_hook(mapping))

    def hook(self, d):
        return self._chain_hooks(self._hooks, d)

    @staticmethod
    def _chain_hooks(hook_funcs, d):
        for hook_func in hook_funcs:
            if d is None:
                return
            d = hook_func(d)
        return d


DATA_JSON_HOOK = chain_hook()
CONF_JSON_HOOK = chain_hook()
DSL_JSON_HOOK = chain_hook()


class Data(object):
    def __init__(self, config: dict, role_str: str):
        self.config = config
        self.role_str = role_str

    @staticmethod
    def load(config, path: Path):
        kwargs = {}
        for field_name in config.keys():
            if field_name not in ["file", "role"]:
                kwargs[field_name] = config[field_name]

        file_path = path.parent.joinpath(config["file"]).resolve()
        if not file_path.exists():
            kwargs["file"] = config["file"]
            # raise ValueError(f"loading from data config: {config} in {path} failed, file: {file_path} not exists")
        else:
            kwargs["file"] = file_path
        role_str = config.get("role") if config.get("role") != "guest" else "guest_0"
        return Data(config=kwargs, role_str=role_str)

    def update(self, config: Config):
        self.config.update(dict(work_mode=config.work_mode, backend=config.backend))


class JobConf(object):
    def __init__(self, initiator: dict, role: dict, job_parameters: dict, **kwargs):
        self.initiator = initiator
        self.role = role
        self.job_parameters = job_parameters
        self.others_kwargs = kwargs

    def as_dict(self):
        return dict(
            initiator=self.initiator,
            role=self.role,
            job_parameters=self.job_parameters,
            **self.others_kwargs,
        )

    @staticmethod
    def load(path: Path):
        with path.open("r") as f:
            kwargs = json.load(f, object_hook=CONF_JSON_HOOK.hook)
        return JobConf(**kwargs)

    @property
    def dsl_version(self):
        return self.others_kwargs.get("dsl_version", 1)

    def update(
        self,
        parties: Parties,
        work_mode,
        backend,
        timeout,
        job_parameters,
        component_parameters,
    ):
        self.initiator = parties.extract_initiator_role(self.initiator["role"])
        self.role = parties.extract_role(
            {role: len(parties) for role, parties in self.role.items()}
        )
        self.update_job_common_parameters(
            work_mode=work_mode, backend=backend, timeout=timeout
        )

        for key, value in job_parameters.items():
            self.update_parameters(parameters=self.job_parameters, key=key, value=value)
        for key, value in component_parameters.items():
            if self.dsl_version == 1:
                self.update_parameters(
                    parameters=self.others_kwargs.get("algorithm_parameters"),
                    key=key,
                    value=value,
                )
            else:
                self.update_parameters(
                    parameters=self.others_kwargs.get("component_parameters"),
                    key=key,
                    value=value,
                )

    def update_parameters(self, parameters, key, value):
        if isinstance(parameters, dict):
            for keys in parameters:
                if keys == key:
                    parameters.get(key).update(value),
                elif isinstance(parameters[keys], dict):
                    self.update_parameters(parameters[keys], key, value)

    def update_job_common_parameters(self, **kwargs):
        if self.dsl_version == 1:
            self.job_parameters.update(**kwargs)
        else:
            self.job_parameters.setdefault("common", {}).update(**kwargs)

    def update_component_parameters(self, key, value, parameters=None):
        if parameters is None:
            if self.dsl_version == 1:
                parameters = self.others_kwargs.get("algorithm_parameters")
            else:
                parameters = self.others_kwargs.get("component_parameters")
        if isinstance(parameters, dict):
            for keys in parameters:
                if keys == key:
                    parameters.update({key: value})
                elif (
                    isinstance(parameters[keys], dict) and parameters[keys] is not None
                ):
                    self.update_component_parameters(key, value, parameters[keys])

    def get_component_parameters(self, keys):
        if self.dsl_version == 1:
            parameters = self.others_kwargs.get("role_parameters")
        else:
            parameters = self.others_kwargs.get("component_parameters").get("role")

        for key in keys:
            parameters = parameters[key]
        return parameters


class JobDSL(object):
    def __init__(self, components: dict):
        self.components = components

    @staticmethod
    def load(path: Path):
        with path.open("r") as f:
            kwargs = json.load(f, object_hook=DSL_JSON_HOOK.hook)
        return JobDSL(**kwargs)

    def as_dict(self):
        return dict(components=self.components)


class Job(object):
    def __init__(
        self,
        job_name: str,
        job_conf: JobConf,
        job_dsl: typing.Optional[JobDSL],
        pre_works: list,
    ):
        self.job_name = job_name
        self.job_conf = job_conf
        self.job_dsl = job_dsl
        self.pre_works = pre_works

    @classmethod
    def load(cls, job_name, job_configs, base: Path):
        job_conf = JobConf.load(base.joinpath(job_configs.get("conf")).resolve())
        job_dsl = job_configs.get("dsl", None)
        if job_dsl is not None:
            job_dsl = JobDSL.load(base.joinpath(job_dsl).resolve())

        pre_works = []
        pre_works_value = []
        name_dict = {}
        if job_configs.get("data_deps", None):
            pre_works_value.append("data_deps")
            assembly = list(job_configs["data_deps"].keys())[0]
            name_dict["data"] = job_configs["data_deps"][assembly]
        if job_configs.get("model_deps", None):
            pre_works_value.append("model_deps")
        if job_configs.get("deps", None):
            pre_works_value.append("model_deps")

        if job_configs.get("model_deps", None):
            pre_works.append(job_configs["model_deps"])
            name_dict["name"] = job_configs["model_deps"]
        elif job_configs.get("deps", None):
            pre_works.append(job_configs["deps"])
            name_dict["name"] = job_configs["deps"]
        elif job_configs.get("data_deps", None):
            pre_works.append(list(job_configs["data_deps"].keys())[0])
            name_dict["name"] = list(job_configs["data_deps"].keys())[0]
        pre_works_value.append(name_dict)
        _config.deps_alter[job_name] = pre_works_value

        return Job(
            job_name=job_name, job_conf=job_conf, job_dsl=job_dsl, pre_works=pre_works
        )

    @property
    def submit_params(self):
        return dict(
            conf=self.job_conf.as_dict(),
            dsl=self.job_dsl.as_dict() if self.job_dsl else None,
        )

    def set_pre_work(self, name, **kwargs):
        self.job_conf.update_job_common_parameters(**kwargs)

    def set_input_data(self, hierarchys, table_info):
        for table_name, hierarchy in zip(table_info, hierarchys):
            key = list(table_name.keys())[0]
            value = table_name[key]
            self.job_conf.update_component_parameters(
                key=key,
                value=value,
                parameters=self.job_conf.get_component_parameters(hierarchy),
            )

    def is_submit_ready(self):
        return len(self.pre_works) == 0


class PipelineJob(object):
    def __init__(self, job_name: str, script_path: Path):
        self.job_name = job_name
        self.script_path = script_path


class Testsuite(object):
    def __init__(
        self,
        dataset: typing.List[Data],
        jobs: typing.List[Job],
        pipeline_jobs: typing.List[PipelineJob],
        path: Path,
    ):
        self.dataset = dataset
        self.jobs = jobs
        self.pipeline_jobs = pipeline_jobs
        self.path = path

        self._dependency: typing.MutableMapping[str, typing.List[Job]] = {}
        self._final_status: typing.MutableMapping[str, FinalStatus] = {}
        self._ready_jobs = deque()
        for job in self.jobs:
            for name in job.pre_works:
                self._dependency.setdefault(name, []).append(job)

            self._final_status[job.job_name] = FinalStatus(job.job_name)
            if job.is_submit_ready():
                self._ready_jobs.appendleft(job)

        for job in self.pipeline_jobs:
            self._final_status[job.job_name] = FinalStatus(job.job_name)

    @staticmethod
    def load(path: Path):
        with path.open("r") as f:
            testsuite_config = json.load(f, object_hook=DATA_JSON_HOOK.hook)

        dataset = []
        for d in testsuite_config.get("data"):
            if "use_local_data" not in d:
                d.update({"use_local_data": _config.use_local_data})
            dataset.append(Data.load(d, path))

        jobs = []
        for job_name, job_configs in testsuite_config.get("tasks", {}).items():
            jobs.append(
                Job.load(job_name=job_name, job_configs=job_configs, base=path.parent)
            )

        pipeline_jobs = []
        for job_name, job_configs in testsuite_config.get("pipeline_tasks", {}).items():
            script_path = path.parent.joinpath(job_configs["script"]).resolve()
            pipeline_jobs.append(PipelineJob(job_name, script_path))

        testsuite = Testsuite(dataset, jobs, pipeline_jobs, path)
        return testsuite

    def jobs_iter(self) -> typing.Generator[Job, None, None]:
        while self._ready_jobs:
            yield self._ready_jobs.pop()

    def pretty_final_summary(self, time_consuming):
        table = prettytable.PrettyTable(
            ["job_name", "job_id", "status", "time_consuming", "exception_id", "rest_dependency"]
        )
        for status in self.get_final_status().values():
            table.add_row(
                [
                    status.name,
                    status.job_id,
                    status.status,
                    time_consuming.pop(0),
                    status.exception_id,
                    ",".join(status.rest_dependency),
                ]
            )
        return table.get_string()

    def model_in_dep(self, name):
        return name in self._dependency

    def get_dependent_jobs(self, name):
        return self._dependency[name]

    def remove_dependency(self, name):
        del self._dependency[name]

    def feed_dep_info(self, job, name, model_info=None, table_info=None):
        if model_info is not None:
            job.set_pre_work(name, **model_info)
        if table_info is not None:
            job.set_input_data(table_info["hierarchy"], table_info["table_info"])
        if name in job.pre_works:
            job.pre_works.remove(name)
        if job.is_submit_ready():
            self._ready_jobs.appendleft(job)

    def reflash_configs(self, config: Config):

        for data in self.dataset:
            data.config.update(dict(work_mode=config.work_mode, backend=config.backend))

        failed = []
        for job in self.jobs:
            try:
                job.job_conf.update(
                    config.parties, config.work_mode, config.backend, None, {}, {}
                )
            except ValueError as e:
                failed.append((job, e))
        return failed

    def update_status(
        self, job_name, job_id: str = None, status: str = None, exception_id: str = None
    ):
        for k, v in locals().items():
            if k != "job_name" and v is not None:
                setattr(self._final_status[job_name], k, v)

    def get_final_status(self):
        for name, jobs in self._dependency.items():
            for job in jobs:
                self._final_status[job.job_name].rest_dependency.append(name)
        return self._final_status


class FinalStatus(object):
    def __init__(
        self,
        name: str,
        job_id: str = "-",
        status: str = "not submitted",
        exception_id: str = "-",
        rest_dependency: typing.List[str] = None,
    ):
        self.name = name
        self.job_id = job_id
        self.status = status
        self.exception_id = exception_id
        self.rest_dependency = rest_dependency or []

class BenchmarkJob(object):
    def __init__(self, job_name: str, script_path: Path, conf_path: Path):
        self.job_name = job_name
        self.script_path = script_path
        self.conf_path = conf_path


class BenchmarkPair(object):
    def __init__(
        self, pair_name: str, jobs: typing.List[BenchmarkJob], compare_setting: dict
    ):
        self.pair_name = pair_name
        self.jobs = jobs
        self.compare_setting = compare_setting


class BenchmarkSuite(object):
    def __init__(
        self, dataset: typing.List[Data], pairs: typing.List[BenchmarkPair], path: Path
    ):
        self.dataset = dataset
        self.pairs = pairs
        self.path = path

    @staticmethod
    def load(path: Path):
        with path.open("r") as f:
            testsuite_config = json.load(f, object_hook=DATA_JSON_HOOK.hook)

        dataset = []
        for d in testsuite_config.get("data"):
            dataset.append(Data.load(d, path))

        pairs = []
        for pair_name, pair_configs in testsuite_config.items():
            if pair_name == "data":
                continue
            jobs = []
            for job_name, job_configs in pair_configs.items():
                if job_name == "compare_setting":
                    continue
                script_path = path.parent.joinpath(job_configs["script"]).resolve()
                if job_configs.get("conf"):
                    conf_path = path.parent.joinpath(job_configs["conf"]).resolve()
                else:
                    conf_path = ""
                jobs.append(
                    BenchmarkJob(
                        job_name=job_name, script_path=script_path, conf_path=conf_path
                    )
                )
            compare_setting = pair_configs.get("compare_setting")
            if compare_setting and not isinstance(compare_setting, dict):
                raise ValueError(
                    f"expected 'compare_setting' type is dict, received {type(compare_setting)} instead."
                )
            pairs.append(
                BenchmarkPair(
                    pair_name=pair_name, jobs=jobs, compare_setting=compare_setting
                )
            )
        suite = BenchmarkSuite(dataset=dataset, pairs=pairs, path=path)
        return suite


def _namespace_hook(namespace):
    def _hook(d):
        if d is None:
            return d
        if "namespace" in d and namespace:
            d["namespace"] = f"{d['namespace']}_{namespace}"
        return d

    return _hook


def _replace_hook(mapping: dict):
    def _hook(d):
        for k, v in mapping.items():
            if k in d:
                d[k] = v
        return d

    return _hook


class JsonParamType(click.ParamType):
    name = "json_string"

    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except ValueError:
            self.fail(f"{value} is not a valid json string", param, ctx)


JSON_STRING = JsonParamType()
