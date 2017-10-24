#!/usr/bin/env bash


dataTime=$(date +%Y%m%d_%H%M%S)

if [ -d /data/code_backup ];then
    :
else
    mkdir -p /data/code_backup
fi

if [ -d /data/deploy ];then
    cd /data
    tar czf /data/code_backup/${dataTime}_deploy.tar.gz deploy
    if [ "$?" -eq 0 ];then
        rm -rf  /data/deploy \
        && if test -L /data/wardata;then rm -rf /data/wardata;fi \
        && if test -d /data/wwwroot;then rm -rf /data/wwwroot/*;fi
        echo "backup and clear old packages success."
    else
        echo "backup and clear old packages failed."
        exit 1
    fi
fi

exit 0