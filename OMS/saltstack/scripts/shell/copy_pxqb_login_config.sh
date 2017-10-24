#!/usr/bin/env bash


projectName=$1
targetPath=$2
zone=$3

appConfigPath='/srv/salt/app_config'
sourcePath=${appConfigPath}/${zone}

if [ -d ${sourcePath} ];then
    cd ${sourcePath}
    if [ -d ${projectName} ];then
        cp -rf ${projectName} ${targetPath}
        if [ $? -eq 0 ];then
            echo "copy success."
        else
            echo "copy failed."
            exit 1
        fi
    else
        echo "${projectName} not found"
        exit 1
    fi
else:
    echo "${sourcePath} not found"
    exit 1
fi

exit 0
