#!/usr/bin/env bash


checkPidExists() {
  if [ -z `pidof redis` ]; then
    return 0
  else
    return 1
  fi
}


rpm -qa |grep supervisor

if [ "$?" -eq 0 ];then
    echo "supervisor is exist"
    checkPidExists
    num=$?
    if [ ${num} -eq 1 ];then
        systemctl start supervisord.service
        if [ $? -eq 0 ];then
            echo "start supervisor success."
        fi
    else
        echo "redis.service is not running. please run first!"
        exit 1
    fi
fi


# yum install supervisor

yum install epel-release -y && yum -y  install supervisor
if [ $? -ne 0 ];then
    echo "yum supervisor fail"
    exit 1
fi

# create file thread.ini

cat > /etc/supervisord.d/thread.ini << EOF
[program:thread]
stdout_logfile=/data/logs/supervisor/thread_stdout.log
command=/usr/local/lnmp/php56/bin/php /data/wwwroot/pxqb_base/bin/thread.php
user=root
autostart=true
autorestart=true
startsecs=3
redirect_stderr=true
EOF

if [ $? -ne 0 ];then
    echo "touch thread.ini failed."
    exit 1
fi

# mkdir supervisor

if [ ! -d /data/logs/supervisor ];then
    mkdir -p /data/logs/supervisor
fi

echo "deploy supervisor successfull"

checkPidExists

num=$?

if [ ${num} -eq 1 ]; then
    systemctl start supervisord.service
    if [ "$?" -eq 0 ]; then
        echo "start supervisor success."
        exit 0
    fi
else
    echo "redis.service is not running. please run first!"
    exit 1
fi

exit 0