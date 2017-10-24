#!/usr/bin/env bash

deploy_path=$1

if [ ! $# -eq 1 ];then
  echo "Usage: $0 { deploy_path } "
  exit
fi

if [ -d ${deploy_path} ]; then
  cd ${deploy_path}
  git pull
else
  echo "this machine not deploy ${deploy_path}, nothing to do!"
fi

exit 0