#!/usr/bin/env bash

srcFile=$1
genFile=$2
domain=$3
zone=$4
templatePath=$5
generatePath=$6


if [ ! $# -eq 6 ];then
    echo "Usage: $0 srcFile genFile domain zone templatePath generatePath"
    exit 1
fi

if [ test -f "${templatePath}/${srcFile}" ];then
    if [  test -d "${generatePath}" ];then
        cp -rf ${templatePath}/${srcFile} ${generatePath}/${genFile}
        cd ${generatePath}
        sed -i "s/localhost/${domain}/g" ${genFile} && \
        sed -i "s/pxqb_login/pxqb_login_${zone}/g" ${genFile} && \
        sed -i "s/vhost_access.log/${zone}_access.log/g" ${genFile}

        if [ $? -eq 0 ];then
            echo "replace done!"
            exit 0
        else
            echo "replace failed!"
            exit 1
        fi

    else
        echo "${generatePath} not found"
        exit 1
    fi
else
    echo "${templatePath}/${srcFile} not found"
    exit 1
fi
