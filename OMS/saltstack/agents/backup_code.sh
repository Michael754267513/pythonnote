#!/bin/sh

backupDir=$1
deployDir=$2
packageName=$3

if [ ! $# -eq 3 ];then
  echo "Usage: $0 { backupDir } { deployDir } { packageName }"
fi

if [ ! -d ${backupDir} ];then
  mkdir -p ${backupDir}
fi

if [ ! -d ${backupDir} ]; then
  mkdir -p ${backupDir}
fi

# backup code skip .git logs directory
if [ -d ${deployDir} ];then
  cd ${deployDir}
else
  echo "No such file or directory"
  exit 1
fi

tar czf ${backupDir}/${packageName} * --exclude='./git' --exclude='log'

if [ $? -eq 0 ];then
  echo "backup success."
  exit 0
else
  echo "backup Failed."
  exit 1
fi