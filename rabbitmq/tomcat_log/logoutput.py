# encoding=utf-8
import subprocess
import pika
import os, sys

logFile = "log"

credentials = pika.PlainCredentials("michael", "michael")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.2.188', credentials=credentials))
channel = connection.channel()


def monitorlog(logFile):
    popen = subprocess.Popen('tail -fn0 ' + logFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while True:
        try:
            message = popen.stdout.readline().strip()
            if message:
                channel.basic_publish(exchange='',
                                      routing_key='test',
                                      body=message)
        except:
            break
    connection.close()


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # 重定向标准文件描述符（默认情况下定向到/dev/null）
    try:
        pid = os.fork()
        # 父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            sys.exit(0)  # 父进程退出
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

        # 从母体环境脱离
    os.chdir("/")  # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.umask(0)  # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()  # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

    # 执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # 第二个父进程退出
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

        # 进程已经是守护进程了，重定向标准文件描述符

    for f in sys.stdout, sys.stderr: f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())  # dup2函数原子化关闭和复制文件描述符
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

if __name__ == '__main__':
    daemonize(stderr="/var/log/rabbit_log/error.log", stdout="/var/log/rabbit_log/access.log")
    monitorlog(logFile)
