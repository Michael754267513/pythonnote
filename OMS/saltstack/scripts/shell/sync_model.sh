#!/usr/bin/env bash

if [ -d '/srv/salt/' ];then
    cp -rf /data/deploy/OMS/saltstack/scripts/_grains /srv/salt/
    if [ "$?" -eq 0 ];then
        echo "copy _grains success."
        salt '*' saltutil.sync_all > /dev/null 2>&1 && salt '*' sys.reload_modules > /dev/null 2>&1
        if [ "$?" -eq 0 ];then
            echo "sync salt util and reload modules success."
        else
            echo "sync salt util and reload modules failed"
            exit 1
        fi
    else
        echo "copy _grains Failed."
        exit 1
    fi
fi
