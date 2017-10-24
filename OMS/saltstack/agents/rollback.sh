#!/usr/bin/env bash


packageName=$1
deployDir=$2

if [ ! $# -eq 2 ];then
  echo "Usage: $0 { packageName } { deployDir }"
  exit 1
fi

if [ ! -f ${packageName} ]; then
  echo "rollback package not found"
  exit 1
fi

if [ ! -d ${deployDir} ];then
  echo "${deployDir} not found"
  exit 1
fi

tar zxvf ${packageName} -C ${deployDir} > /dev/null 2>&1

if [ $? -eq 0 ];then
  echo "rollback success."
  exit 0
else
  echo "rollback Failed."
  exit 1
fi