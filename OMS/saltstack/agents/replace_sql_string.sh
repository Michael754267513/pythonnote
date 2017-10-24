#!/usr/bin/env bash

baseName=$1
zoneId=$2
zoneName=$3
startDate=$4
startTime=$5
mysql_address=$6
mysql_password=$7


# import sql
import_sql(){
    database=$1
    if [ -f /usr/local/lnmp/mysql/bin/mysql ];then
        /usr/local/lnmp/mysql/bin/mysql -h${mysql_address} -uroot -p${mysql_password} < ${database}
        if [ "$?" -eq 0 ];then
            echo "import database success."
        else
            echo "import database failed."
            exit 1
        fi
    else
        echo "/usr/local/lnmp/mysql/bin/mysql Not Found!"
        exit 1
    fi
}

# git clone sql

git_clone_sql()
{
    if [ -d /home/update_sql ];then
        cd /home/update_sql && git pull
    else
        if [ -f /bin/git ];then
            git clone https://zhoufr:NkdpDxHNLqZH@git.pythonic.in/wuhan/pxqb_sql.git /home/update_sql
            if [ $? -eq 0 ];then
                echo "download sql success."
            else
                echo "download sql failed."
                exit 1
            fi
        fi
    fi
}


if [ ! $# -eq 7 ];then
  echo "Usage: $0 fileName zoneId zoneName startDate startTime mysql_address mysql_pass"
  exit 1
fi

git_clone_sql

cd /home/update_sql

if [ -f "${baseName}" ];then
    cp ${baseName} ${zoneId}_${baseName}
    if [ $? -eq 0 ];then
        echo "copy success."
    fi
else
    echo "${baseName} not found"
    exit 1
fi

if [ ! -f ${zoneId}_${baseName} ];then
  echo "${zoneId}_${baseName} not found"
  exit 1
else
  sed -i "s/%__PXQB_SERVERID__%/${zoneId}/g" ${zoneId}_${baseName}
  if [ $? -eq 0 ];then
    echo "replace %__PXQB_SERVERID__% to ${zoneId} done!"
  else
    exit 1
  fi

  sed -i "s/%__PXQB_SERVERNAME__%/${zoneName}/g" ${zoneId}_${baseName}
  if [ $? -eq 0 ];then
    echo "replace %__PXQB_SERVERNAME__% to ${zoneName} done!"
  else
    exit 1
  fi

  sed -i "s/%__PXQB_SERVERDAY__%/${startDate}/g" ${zoneId}_${baseName}
  if [ $? -eq 0 ];then
    echo "replace %__PXQB_SERVERDAY__% to ${startDate} done!"
  else
    exit 1
  fi

  sed -i "s/%__PXQB_SERVERTIME__%/${startTime}/g" ${zoneId}_${baseName}
  if [ $? -eq 0 ];then
    echo "replace %__PXQB_SERVERTIME__% to ${startTime} done!"
  else
    exit 1
  fi
fi

import_sql ${zoneId}_${baseName}

exit 0