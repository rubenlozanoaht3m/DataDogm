#!/bin/bash

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

set -e
cwd=$(cd `dirname $0`; pwd)
cd ${cwd}
source_code_dir=$(cd `dirname ${cwd}`; cd ../; pwd)
echo "[INFO] Source code dir is ${source_code_dir}"
packages_dir=${source_code_dir}/cluster-deploy/packages
mkdir -p ${packages_dir}
source ./default_configurations.sh

cd ${source_code_dir}
eggroll_git_url=`grep -A 3 '"eggroll"' .gitmodules | grep 'url' | awk -F '= ' '{print $2}'`
eggroll_git_branch=`grep -A 3 '"eggroll"' .gitmodules | grep 'branch' | awk -F '= ' '{print $2}'`
echo "[INFO] Git clone eggroll submodule source code from ${eggroll_git_url} branch ${eggroll_git_branch}"
if [[ -e "eggroll" ]];then
    while [[ true ]];do
        read -p "The eggroll directory already exists, delete and re-download? [y/n] " input
        case ${input} in
        [yY]*)
                echo "[INFO] Delete the original eggroll"
                rm -rf eggroll
                git clone ${eggroll_git_url} -b ${eggroll_git_branch} eggroll
                break
                ;;
        [nN]*)
                echo "[INFO] Use the original eggroll"
                break
                ;;
        *)
                echo "Just enter y or n, please."
                ;;
        esac
    done
else
    git clone ${eggroll_git_url} -b ${eggroll_git_branch} eggroll
fi

eggroll_source_code_dir=${source_code_dir}/eggroll
cd ${eggroll_source_code_dir}
echo "[INFO] Compiling eggroll"
mvn clean package -DskipTests
echo "[INFO] Compile eggroll done"

echo "[INFO] Packaging eggroll"
cd ${eggroll_source_code_dir}
cd api
tar czf eggroll-api-1.1.tar.gz *
mv eggroll-api-1.1.tar.gz ${packages_dir}/

cd ${eggroll_source_code_dir}
cd computing
tar czf eggroll-computing-1.1.tar.gz *
mv eggroll-computing-1.1.tar.gz ${packages_dir}/

cd ${eggroll_source_code_dir}
cd conf
tar czf eggroll-conf-1.1.tar.gz *
mv eggroll-conf-1.1.tar.gz ${packages_dir}/

cd ${eggroll_source_code_dir}
cd framework/egg/target
tar czf eggroll-egg-1.1.tar.gz eggroll-egg-1.1.jar lib/
mv eggroll-egg-1.1.tar.gz ${packages_dir}/

cd ${eggroll_source_code_dir}
cd framework/meta-service/target
tar czf eggroll-meta-service-1.1.tar.gz eggroll-meta-service-1.1.jar lib/
mv eggroll-meta-service-1.1.tar.gz ${packages_dir}/

cd ${eggroll_source_code_dir}
cd framework/roll/target
tar czf eggroll-roll-1.1.tar.gz eggroll-roll-1.1.jar lib/
mv eggroll-roll-1.1.tar.gz ${packages_dir}/

cd ${eggroll_source_code_dir}
cd storage/storage-service-cxx
tar czf eggroll-storage-service-cxx-1.1.tar.gz *
mv eggroll-storage-service-cxx-1.1.tar.gz ${packages_dir}/
echo "[INFO] Package eggroll done"

cd ${source_code_dir}
fateboard_git_url=`grep -A 3 '"fateboard"' .gitmodules | grep 'url' | awk -F '= ' '{print $2}'`
fateboard_git_branch=`grep -A 3 '"fateboard"' .gitmodules | grep 'branch' | awk -F '= ' '{print $2}'`
echo "[INFO] Git clone fateboard submodule source code from ${fateboard_git_url} branch ${fateboard_git_branch}"
if [[ -e "fateboard" ]];then
    while [[ true ]];do
        read -p "The fateboard directory already exists, delete and re-download? [y/n] " input
        case ${input} in
        [yY]*)
                echo "[INFO] Delete the original fateboard"
                rm -rf fateboard
                git clone ${fateboard_git_url} -b ${fateboard_git_branch} fateboard
                break
                ;;
        [nN]*)
                echo "[INFO] Use the original fateboard"
                break
                ;;
        *)
                echo "Just enter y or n, please."
                ;;
        esac
    done
else
    git clone ${fateboard_git_url} -b ${fateboard_git_branch} fateboard
fi

echo "[INFO] Compiling fate"
cd ${source_code_dir}/fateboard/
mvn clean package -DskipTests
cd ${source_code_dir}/arch/
mvn clean package -DskipTests
echo "[INFO] Compile fate done"

echo "[INFO] Packaging fate"
cp ${source_code_dir}/fateboard/target/fateboard-1.1.jar ${packages_dir}/

cd ${source_code_dir}/arch/driver/federation/target
tar czf fate-federation-1.1.tar.gz fate-federation-1.1.jar lib/
mv fate-federation-1.1.tar.gz ${packages_dir}/

cd ${source_code_dir}/arch/networking/proxy/target
tar czf fate-proxy-1.1.tar.gz fate-proxy-1.1.jar lib/
mv fate-proxy-1.1.tar.gz ${packages_dir}/

echo "[INFO] Packaging base module"
get_module_package ${source_code_dir} "python" pip-packages-fate-${python_version}.tar.gz
get_module_package ${source_code_dir} "python" Miniconda3-4.5.4-Linux-x86_64.sh
get_module_package ${source_code_dir} "jdk" jdk-${jdk_version}-linux-x64.tar.gz
get_module_package ${source_code_dir} "mysql" mysql-${mysql_version}-linux-glibc2.12-x86_64.tar.xz
get_module_package ${source_code_dir} "redis" redis-${redis_version}.tar.gz
get_module_package ${source_code_dir} "storage-service-cxx third-party" third_party_eggrollv1.tar.gz
echo "[INFO] Package base module done"
echo "[INFO] Package fate done"
echo "[INFO] A total of `ls ${packages_dir} | wc -l | awk '{print $1}'` packages:"
ls -lrt ${packages_dir}
