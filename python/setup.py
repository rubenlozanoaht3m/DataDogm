# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arch',
 'arch.api',
 'arch.api.utils',
 'fate_arch',
 'fate_arch.abc',
 'fate_arch.common',
 'fate_arch.computing',
 'fate_arch.computing.eggroll',
 'fate_arch.computing.spark',
 'fate_arch.computing.standalone',
 'fate_arch.federation',
 'fate_arch.federation.eggroll',
 'fate_arch.federation.rabbitmq',
 'fate_arch.federation.pulsar',
 'fate_arch.federation.standalone',
 'fate_arch.federation.transfer_variable',
 'fate_arch.federation.transfer_variable.scripts',
 'fate_arch.protobuf.python',
 'fate_arch.session',
 'fate_arch.storage',
 'fate_arch.storage.eggroll',
 'fate_arch.storage.file',
 'fate_arch.storage.hdfs',
 'fate_arch.storage.metastore',
 'fate_arch.storage.mysql',
 'fate_arch.storage.standalone',
 'fate_flow',
 'fate_flow.apps',
 'fate_flow.components',
 'fate_flow.components.param',
 'fate_flow.controller',
 'fate_flow.db',
 'fate_flow.entity',
 'fate_flow.examples',
 'fate_flow.examples.manage_mq',
 'fate_flow.manager',
 'fate_flow.operation',
 'fate_flow.pipelined_model',
 'fate_flow.scheduler',
 'fate_flow.scheduling_apps',
 'fate_flow.scheduling_apps.client',
 'fate_flow.tests',
 'fate_flow.tests.api_tests',
 'fate_flow.utils',
 'federatedml',
 'federatedml.conf',
 'federatedml.ensemble',
 'federatedml.ensemble.basic_algorithms',
 'federatedml.ensemble.basic_algorithms.decision_tree',
 'federatedml.ensemble.basic_algorithms.decision_tree.hetero',
 'federatedml.ensemble.basic_algorithms.decision_tree.homo',
 'federatedml.ensemble.basic_algorithms.decision_tree.tree_core',
 'federatedml.ensemble.boosting.boosting_core',
 'federatedml.ensemble.boosting.hetero',
 'federatedml.ensemble.boosting.homo',
 'federatedml.ensemble.images',
 'federatedml.ensemble.test',
 'federatedml.evaluation',
 'federatedml.evaluation.metrics',
 'federatedml.evaluation.test',
 'federatedml.feature',
 'federatedml.feature.binning',
 'federatedml.feature.binning.optimal_binning',
 'federatedml.feature.binning.test',
 'federatedml.feature.binning.test.test_optimal_binning',
 'federatedml.feature.binning.test.test_quantile_binning_module',
 'federatedml.feature.feature_scale',
 'federatedml.feature.feature_scale.test',
 'federatedml.feature.feature_selection',
 'federatedml.feature.feature_selection.model_adapter',
 'federatedml.feature.feature_selection.test',
 'federatedml.feature.hetero_feature_binning',
 'federatedml.feature.hetero_feature_selection',
 'federatedml.feature.homo_feature_binning',
 'federatedml.feature.homo_onehot',
 'federatedml.feature.test',
 'federatedml.feature.test.test_new_binning',
 'federatedml.feature.test.test_new_feature_selection',
 'federatedml.framework',
 'federatedml.framework.hetero',
 'federatedml.framework.hetero.procedure',
 'federatedml.framework.hetero.sync',
 'federatedml.framework.hetero.util',
 'federatedml.framework.homo',
 'federatedml.framework.homo.blocks',
 'federatedml.framework.homo.procedure',
 'federatedml.framework.homo.test',
 'federatedml.framework.homo.test.blocks',
 'federatedml.framework.homo.util',
 'federatedml.framework.test',
 'federatedml.framework.test.homo',
 'federatedml.linear_model',
 'federatedml.linear_model.linear_regression',
 'federatedml.linear_model.linear_regression.hetero_linear_regression',
 'federatedml.linear_model.linear_regression.images',
 'federatedml.linear_model.logistic_regression',
 'federatedml.linear_model.logistic_regression.hetero_logistic_regression',
 'federatedml.linear_model.logistic_regression.homo_logsitic_regression',
 'federatedml.linear_model.logistic_regression.images',
 'federatedml.linear_model.poisson_regression',
 'federatedml.linear_model.poisson_regression.hetero_poisson_regression',
 'federatedml.linear_model.poisson_regression.images',
 'federatedml.local_baseline',
 'federatedml.local_baseline.test',
 'federatedml.loss',
 'federatedml.loss.test',
 'federatedml.model_selection',
 'federatedml.model_selection.data_split',
 'federatedml.model_selection.data_split.test',
 'federatedml.model_selection.stepwise',
 'federatedml.model_selection.stepwise.test',
 'federatedml.model_selection.test',
 'federatedml.nn',
 'federatedml.nn.backend',
 'federatedml.nn.backend.pytorch',
 'federatedml.nn.backend.tf',
 'federatedml.nn.backend.tf_keras',
 'federatedml.nn.backend.tf_keras.layers',
 'federatedml.nn.hetero_nn',
 'federatedml.nn.hetero_nn.backend',
 'federatedml.nn.hetero_nn.backend.tf_keras',
 'federatedml.nn.hetero_nn.backend.tf_keras.interactive',
 'federatedml.nn.hetero_nn.images',
 'federatedml.nn.hetero_nn.model',
 'federatedml.nn.hetero_nn.test',
 'federatedml.nn.hetero_nn.util',
 'federatedml.nn.homo_nn',
 'federatedml.nn.homo_nn.demo',
 'federatedml.nn.homo_nn.demo.mnist',
 'federatedml.nn.test',
 'federatedml.nn.zoo',
 'federatedml.one_vs_rest',
 'federatedml.optim',
 'federatedml.optim.gradient',
 'federatedml.optim.gradient.test',
 'federatedml.optim.images',
 'federatedml.optim.test',
 'federatedml.param',
 'federatedml.param.test',
 'federatedml.protobuf',
 'federatedml.protobuf.generated',
 'federatedml.protobuf.homo_model_convert',
 'federatedml.protobuf.homo_model_convert.pytorch',
 'federatedml.protobuf.homo_model_convert.sklearn',
 'federatedml.protobuf.homo_model_convert.tf_keras',
 'federatedml.protobuf.model_migrate',
 'federatedml.protobuf.model_migrate.converter',
 'federatedml.protobuf.test',
 'federatedml.secure_information_retrieval',
 'federatedml.secureprotol',
 'federatedml.secureprotol.number_theory',
 'federatedml.secureprotol.number_theory.field',
 'federatedml.secureprotol.number_theory.group',
 'federatedml.secureprotol.oblivious_transfer',
 'federatedml.secureprotol.oblivious_transfer.hauck_oblivious_transfer',
 'federatedml.secureprotol.random_oracle',
 'federatedml.secureprotol.random_oracle.hash_function',
 'federatedml.secureprotol.random_oracle.message_authentication_code',
 'federatedml.secureprotol.spdz',
 'federatedml.secureprotol.spdz.beaver_triples',
 'federatedml.secureprotol.spdz.communicator',
 'federatedml.secureprotol.spdz.tensor',
 'federatedml.secureprotol.spdz.test',
 'federatedml.secureprotol.spdz.utils',
 'federatedml.secureprotol.symmetric_encryption',
 'federatedml.secureprotol.test',
 'federatedml.statistic',
 'federatedml.statistic.correlation',
 'federatedml.statistic.intersect',
 'federatedml.statistic.intersect.rsa_cache',
 'federatedml.statistic.intersect.test',
 'federatedml.statistic.psi',
 'federatedml.statistic.psi.test',
 'federatedml.statistic.scorecard',
 'federatedml.statistic.test',
 'federatedml.statistic.union',
 'federatedml.test',
 'federatedml.toy_example',
 'federatedml.transfer_learning',
 'federatedml.transfer_learning.hetero_ftl',
 'federatedml.transfer_learning.hetero_ftl.test',
 'federatedml.transfer_variable',
 'federatedml.transfer_variable.transfer_class',
 'federatedml.unsupervised_learning.kmeans',
 'federatedml.unsupervised_learning.kmeans.hetero_kmeans',
 'federatedml.util',
 'federatedml.util.test']

package_data = \
{'': ['*'],
 'fate_arch': ['protobuf/*', 'protobuf/proto/*'],
 'fate_flow': ['doc/*',
               'images/*',
               'upgrade/1_4_0-1_4_1/*',
               'upgrade/1_4_1-1_4_2/*',
               'upgrade/1_4_x/*'],
 'federatedml': ['unsupervised_learning/image/*'],
 'federatedml.conf': ['setting_conf/*'],
 'federatedml.feature': ['images/*'],
 'federatedml.framework.homo': ['images/*'],
 'federatedml.nn.homo_nn': ['images/*'],
 'federatedml.protobuf': ['proto/*'],
 'federatedml.statistic.correlation': ['img/*'],
 'federatedml.statistic.intersect': ['images/*'],
 'federatedml.transfer_learning.hetero_ftl': ['images/*'],
 'federatedml.transfer_variable': ['auth_conf/*']}

install_requires = \
['apsw==3.9.2.post1',
 'beautifultable==1.0.0',
 'cachetools==3.0.0',
 'cloudpickle==0.6.1',
 'cos-python-sdk-v5==1.8.0',
 'flask==1.0.2',
 'gmpy2==2.0.8',
 'joblib==1.0.1',
 'kazoo==2.6.1',
 'kfserving>=0.5.1'
 'kubernetes>=12.0.1'
 'lmdb==0.94',
 'numpy==1.18.4',
 'minio>=6.0.2',
 'pandas==0.23.4',
 'peewee==3.9.3',
 'psutil==5.6.6',
 'pycryptodomex==3.6.6',
 'python-dotenv==0.13.0',
 'redis==3.0.1',
 'requests-toolbelt==0.9.1',
 'requests==2.23.0',
 'ruamel-yaml==0.16.10',
 'scikit-learn==0.19.2',
 'scipy==1.1.0',
 'tensorflow==1.15.4',
 'torch==1.4.0',
 'torch-model-archiver==0.3.1'
 'torchvision==0.5.0',
 'werkzeug==0.15.3']

setup_kwargs = {
    'name': 'fate',
    'version': '1.5.0',
    'description': "FATE (Federated AI Technology Enabler) is an open-source project initiated by Webank's AI Department to provide a secure computing framework to support the federated AI ecosystem. It implements secure computation protocols based on homomorphic encryption and multi-party computation (MPC). It supports federated learning architectures and secure computation of various machine learning algorithms, including logistic regression, tree-based algorithms, deep learning and transfer learning.",
    'long_description': '[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![CodeStyle](https://img.shields.io/badge/Check%20Style-Google-brightgreen)](https://checkstyle.sourceforge.io/google_style.html) [![Style](https://img.shields.io/badge/Check%20Style-Black-black)](https://checkstyle.sourceforge.io/google_style.html) [![Build Status](https://travis-ci.org/FederatedAI/FATE.svg?branch=develop-1.5-preview)](https://travis-ci.org/FederatedAI/FATE)\n[![codecov](https://codecov.io/gh/FederatedAI/FATE/branch/develop-1.5-preview/graph/badge.svg)](https://codecov.io/gh/FederatedAI/FATE)\n[![Documentation Status](https://readthedocs.org/projects/fate/badge/?version=latest)](https://fate.readthedocs.io/en/latest/?badge=latest)\n\n<div align="center">\n  <img src="./doc/images/FATE_logo.png">\n</div>\n\n[DOC](./doc) | [Quick Start](./examples/dsl/v2) | [中文](./README_zh.md)\n\nFATE (Federated AI Technology Enabler) is an open-source project initiated by Webank\'s AI Department to provide a secure computing framework to support the federated AI ecosystem. It implements secure computation protocols based on homomorphic encryption and multi-party computation (MPC). It supports federated learning architectures and secure computation of various machine learning algorithms, including logistic regression, tree-based algorithms, deep learning and transfer learning.\n\n<https://fate.fedai.org>\n\n\n## Federated Learning Algorithms In FATE\nFATE already supports a number of federated learning algorithms, including vertical federated learning, horizontal federated learning, and federated transfer learning. More details are available in [federatedml](./python/federatedml).\n\n\n## Install\n\nFATE can be installed on Linux or Mac. Now, FATE can support：\n\n* Native installation: standalone and cluster deployments;\n\n* KubeFATE installation:\n\n\t- Multipal parties deployment by docker-compose, which for devolopment and test purpose;\n\n\t- Cluster (multi-node) deployment by Kubernetes\n\n### Native installation:\nSoftware environment :jdk1.8+、Python3.6、python virtualenv、mysql5.6+\n\n##### Standalone\nFATE provides Standalone runtime architecture for developers. It can help developers quickly test FATE. Standalone support two types of deployment: Docker version and Manual version. Please refer to Standalone deployment guide: [standalone-deploy](./standalone-deploy/)\n\n##### Cluster\nFATE also provides a distributed runtime architecture for Big Data scenario. Migration from standalone to cluster requires configuration change only. No algorithm change is needed.\n\nTo deploy FATE on a cluster, please refer to cluster deployment guide: [cluster-deploy](./cluster-deploy).\n\n### KubeFATE installation:\nUsing KubeFATE, FATE can be deployed by either docker-compose or Kubernetes:\n\n* For development or testing purposes, docker-compose is recommended. It only requires Docker enviroment. For more detail, please refer to [Deployment by Docker Compose](https://github.com/FederatedAI/KubeFATE/tree/master/docker-deploy).\n\n* For a production or a large scale deployment, Kubernetes is recommended as an underlying infrastructure to manage FATE system. For more detail, please refer to [Deployment on Kubernetes](https://github.com/FederatedAI/KubeFATE/blob/master/k8s-deploy).\n\nMore instructions can be found in [KubeFATE](https://github.com/FederatedAI/KubeFATE).\n\n### FATE-Client Installation\nFATE-client is a easy tool for interacting with FATE. We strongly recommend you install FATE-client and take advantage to use FATE conveniently. Please refer to this [document](./python/fate_client/README.rst) for more details of FATE-client.\n\n\n## Running Tests\n\nA script to run all the unittests has been provided in ./federatedml/test folder.\n\nOnce FATE is installed, tests can be run using:\n\n> sh ./federatedml/test/run_test.sh\n\nAll the unittests shall pass if FATE is installed properly.\n\n## Example Programs\n\n### Quick Start\n\nWe have provided a tutorial for quick starting modeling task. Please refer ["here"](./examples/pipeline/README.rst)\n\n###  Obtain Model and Check Out Results\nWe provided functions such as tracking component output models or logs etc. through a tool called fate-flow. The deployment and usage of fate-flow can be found [here](./python/fate_flow/README.md)\n\n\n## Doc\n### API doc\nFATE provides some API documents in [doc-api](https://fate.readthedocs.io/en/latest/?badge=latest)\n### Develop Guide doc\nHow to develop your federated learning algorithm using FATE? you can see FATE develop guide document in [develop-guide](./doc/develop_guide.rst)\n### Other doc\nFATE also provides many other documents in [doc](./doc/). These documents can help you understand FATE better.\n\n## Getting Involved\n\n*  Join our maillist [Fate-FedAI Group IO](https://groups.io/g/Fate-FedAI). You can ask questions and participate in the development discussion.\n\n*  For any frequently asked questions, you can check in [FAQ](https://github.com/FederatedAI/FATE/wiki).\n\n*  Please report bugs by submitting [issues](https://github.com/FederatedAI/FATE/issues).\n\n*  Submit contributions using [pull requests](https://github.com/FederatedAI/FATE/pulls)\n\n\n### License\n[Apache License 2.0](LICENSE)\n\n',
    'author': 'FederatedAI',
    'author_email': 'contact@FedAI.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fate.fedai.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
