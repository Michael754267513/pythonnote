#!/usr/bin/env bash


ServerID=$1
FileName=$2

if [ ! $# -eq 2 ];then
    echo "Usage: $0 ServerID FileName"
    exit 1
fi

sed  -i "s#// define('_SERVER_ID',${ServerID});#define('_SERVER_ID',${ServerID});#g" ${FileName}

if [ $? -eq 0 ];then
    echo "enable entrance success"
else
    echo "enable entrance failed!"
    exit 1
fi

exit 0