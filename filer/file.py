# encoding=utf-8
import subprocess

logFile = 'test2.log'


def monitorLog(logFile):
    print '监控的日志文件 是%s' % logFile
    popen = subprocess.Popen('tail -f ' + logFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    pid = popen.pid
    print('Popen.pid:' + str(pid))
    while True:
        line = popen.stdout.readline().strip()
        # 判断内容是否为空
        if line:
            print(line)
    monitorLog(logFile)


if __name__ == '__main__':
    monitorLog(logFile)