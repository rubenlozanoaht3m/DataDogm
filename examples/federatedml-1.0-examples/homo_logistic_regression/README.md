## Homo Logistic Regression Configuration Usage Guide.

This section introduces the dsl and conf for usage of different type of task.

#### Training Task.

1. Train_task:
    dsl: test_homolr_train_job_dsl.json
    runtime_config : test_homolr_train_job_conf.json
   
2. Train, test and evaluation task:
    dsl: test_homolr_evaluate_job_dsl.json
    runtime_config: test_homolr_evaluate_job_conf.json
   
3. Cross Validation Task:
    dsl: test_homolr_cv_job_dsl.json
    runtime_config: test_homolr_cv_job_conf.json

    
Users can use following commands to running the task.
    
    python {fate_install_path}/fate_flow/fate_flow_client.py -f submit_job -c ${runtime_config} -d ${dsl}

Moreover, after successfully running the training task, you can use it to predict too. Read more  [here](../PREDICT_TASK_README.md)
