#!/bin/bash

set -e
module_name="roll"
cwd=$(cd `dirname $0`; pwd)
cd ${cwd}
source ./configurations.sh

usage() {
	echo "usage: $0 {binary/build} {packaging|config|install|init} {configurations path}."
}

deploy_mode=$1
config_path=$3
if [[ ${config_path} == "" ]] || [[ ! -f ${config_path} ]]
then
	usage
	exit
fi
source ${config_path}

packaging() {
    source ../../../default_configurations.sh
    package_init ${output_packages_dir} ${module_name}
    if [[ "${deploy_mode}" == "binary" ]]; then
        get_module_binary ${source_code_dir} ${module_name} eggroll-${module_name}-${version}.tar.gz
        tar xzf eggroll-${module_name}-${version}.tar.gz
        rm -rf eggroll-${module_name}-${version}.tar.gz
    elif [[ "${deploy_mode}" == "build" ]]; then
        cp ${source_code_dir}/eggroll/framework/${module_name}/target/eggroll-${module_name}-${version}.jar ./
        cp -r ${source_code_dir}/eggroll/framework/${module_name}/target/lib ./
    fi
}



config() {
    config_label=$4
	cd ${output_packages_dir}/config/${config_label}
    cd ./${module_name}/conf
	cp ${source_code_dir}/cluster-deploy/scripts/deploy/eggroll/services.sh ./
    sed -i.bak "s#JAVA_HOME=.*#JAVA_HOME=${java_dir}#g" ./services.sh
    sed -i.bak "s#installdir=.*#installdir=${deploy_dir}#g" ./services.sh

    mkdir conf
    cp  ${source_code_dir}/eggroll/framework/${module_name}/src/main/resources/roll.properties ./conf
    cp  ${source_code_dir}/eggroll/framework/${module_name}/src/main/resources/log4j2.properties ./conf
    cp  ${source_code_dir}/eggroll/framework/${module_name}/src/main/resources/applicationContext-roll.xml ./conf

    sed -i.bak "s/party.id=.*/party.id=${party_id}/g" ./conf/roll.properties
    sed -i.bak "s/service.port=.*/service.port=${port}/g" ./conf/roll.properties
    sed -i.bak "s/meta.service.ip=.*/meta.service.ip=${meta_service_ip}/g" ./conf/roll.properties
    sed -i.bak "s/meta.service.port=.*/meta.service.port=${meta_service_port}/g" ./conf/roll.properties
}

init() {
    return 0
}

install(){
    mkdir -p ${deploy_dir}/
    cp -r ${deploy_packages_dir}/source/${module_name} ${deploy_dir}/
    cp -r ${deploy_packages_dir}/config/${module_name}/conf/* ${deploy_dir}/${module_name}
    cd ${deploy_dir}/${module_name}
    ln -s eggroll-${module_name}-${version}.jar eggroll-${module_name}.jar
    mv ./services.sh ${deploy_dir}/
}

case "$2" in
    packaging)
        packaging $*
        ;;
    config)
        config $*
        ;;
    install)
        install $*
        ;;
    init)
        init $*
        ;;
 *)
     usage
        exit -1
esac