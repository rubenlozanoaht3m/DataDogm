import argparse
import json
import os
import time
import traceback

from examples.test import submit

TEST_SUITE_SUFFIX = "testsuite.json"


def search_testsuite(file_dir, suffix=TEST_SUITE_SUFFIX):
    testsuites = []
    for root, dirs, files in os.walk(file_dir):
        for file_name in files:
            if file_name.endswith(suffix):
                path = os.path.join(root, file_name)
                testsuites.append(path)
    return testsuites


def role_map(env, role):
    _role, num = role.split("_", 1)
    loc = env["role"][_role][int(num)]
    return env["ip_map"][str(loc)]


def data_upload(submitter, env, task_data, check_interval=3):
    for data in task_data:
        host = role_map(env, data["role"])
        remote_host = None if host == -1 else host
        format_msg = f"@{data['role']}:{data['file']} >> {data['namespace']}.{data['table_name']}"
        print(f"[{time.strftime('%Y-%m-%d %X')}]uploading {format_msg}")
        job_id = submitter.run_upload(data_path=data["file"], config=data, remote_host=remote_host)
        if not remote_host:
            submitter.await_finish(job_id, check_interval=check_interval)
        else:
            print("warning: not check remote uploading status!!!")
        print(f"[{time.strftime('%Y-%m-%d %X')}]upload done {format_msg}, job_id={job_id}\n")


def run_task(submitter, conf, submit_type, err_name, task_name, check_interval,
             dsl=None,
             model_info=None,
             substitute=None):
    model = None
    # noinspection PyBroadException
    try:
        print(f"[{time.strftime('%Y-%m-%d %X')}][{task_name}]submitting...")
        if submit_type == "train":
            output = submitter.submit_job(conf, submit_type=submit_type, dsl_path=dsl, substitute=substitute)
            model = output['model_info']
        else:
            output = submitter.submit_job(conf, submit_type=submit_type, model_info=model_info, substitute=substitute)
        job_id = output['jobId']
        print(f"[{time.strftime('%Y-%m-%d %X')}][{task_name}]submit done, job_id={job_id}")

        status = submitter.await_finish(job_id, check_interval=check_interval, task_name=task_name)
        result = f"{task_name}\t{status}\t{job_id}"

    except Exception:
        err_msg = traceback.format_exc()
        print(f"[{time.strftime('%Y-%m-%d %X')}][{task_name}]task fail")
        print(err_msg)
        result = f"{task_name}\tsubmit_fail\t"
        with open(f"{err_name}", "a") as f:
            f.write(f"{task_name}\n")
            f.write("===========\n")
            f.write(err_msg)
            f.write("\n")

    return result, model


def run_testsuite(submitter, env, file_name, err_name, check_interval=3, skip_data=False):
    results = []
    models = {}
    testsuite_base_path = os.path.dirname(file_name)

    def check(field_name, config):
        if field_name not in config:
            raise ValueError(f"{field_name} not specified in {task_name}@{file_name}")

    with open(file_name) as f:
        configs = json.loads(f.read())

    if not skip_data:
        data_upload(submitter=submitter, env=env, task_data=configs["data"], check_interval=check_interval)

    for task_name, task_config in configs["tasks"].items():
        check("conf", task_config)
        conf = os.path.join(testsuite_base_path, task_config["conf"])
        dep_task = task_config.get("deps", None)
        sub_tasks = task_config.get("substitutes", {})
        substitute_map = {task_name: None}
        for sub_name, substitute in sub_tasks.items():
            substitute_map[f"{task_name}.{sub_name}"] = substitute

        for sub_task_name, substitute in substitute_map.items():
            if dep_task is None:
                check("dsl", task_config)
                dsl = os.path.join(testsuite_base_path, task_config["dsl"])
                result, model = run_task(submitter, conf, "train", err_name, sub_task_name, check_interval,
                                         dsl=dsl,
                                         substitute=substitute)
                models[sub_task_name] = model
            else:
                if dep_task not in models:
                    results.append(f"{sub_task_name}\t{dep_task} not found")
                    continue
                result, _ = run_task(submitter, conf, "predict", err_name, sub_task_name, check_interval,
                                     model_info=models[dep_task])
            results.append(result)
    return results


def main():
    fate_home = os.path.abspath(f"{os.getcwd()}/../")
    example_path = "federatedml-1.x-examples"

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("env_conf", type=str, help="file to read env config")
    arg_parser.add_argument("-o", "--output", type=str, help="file to save result, defaults to `test_result`",
                            default="test_result")
    arg_parser.add_argument("-e", "--error", type=str, help="file to save error")
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--dir", type=str, help="dir to find testsuites",
                       default=os.path.join(fate_home, example_path))
    group.add_argument("-s", "--suite", type=str, help="testsuite to run")
    arg_parser.add_argument("-i", "--interval", type=int, help="check job status every i seconds, defaults to 1",
                            default=1)
    arg_parser.add_argument("--skip_data", help="skip data upload", action="store_true")
    args = arg_parser.parse_args()

    env_conf = args.env_conf
    output_file = args.output
    err_output = args.error or f"{output_file}.err"
    testsuites_dir = args.dir
    suite = args.suite
    interval = args.interval
    skip_data = args.skip_data

    submitter = submit.Submitter(fate_home=fate_home, work_mode=0)

    try:
        with open(env_conf) as e:
            env = json.loads(e.read())
    except:
        raise ValueError(f"invalid env conf: {env_conf}")
    testsuites = [suite] if suite else search_testsuite(testsuites_dir)

    for file_name in testsuites:
        print(f"[{time.strftime('%Y-%m-%d %X')}]running testsuite {file_name}")
        print("====================================================================\n")
        try:
            results = run_testsuite(submitter, env, file_name, err_output,
                                    check_interval=interval,
                                    skip_data=skip_data)

            with open(output_file, "w") as f:
                f.write(f"{file_name}\n")
                f.write("====================================================================\n")
                for result in results:
                    f.write(f"{result}\n")
                f.write("\n")
        except Exception as e:
            print(f"errors in {file_name}, {e.args}")
        print("\n")


if __name__ == "__main__":
    main()
