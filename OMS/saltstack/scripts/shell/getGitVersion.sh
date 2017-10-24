#!/bin/sh

archivePath=$1

if [ ! $# -eq 1 ];then
  echo "usage: $0 {archivePath}"
  exit 1
fi

if [ -d "$archivePath" ];then
  cd "$archivePath" && git pull
  if [ $? -eq 0 ];then
    git log --pretty=format:"%h %ad%x09%an%x09%s" --date=short | awk 'BEGIN{min=1;max=1}{if(NR>=min){if(NR<=max)print}}'
    exit 0
  else
    exit 1
  fi
else
  echo "No such file or directory"
  exit 1
fi