#!/usr/bin/python
# --*-- coding:utf8 --*--


import paramiko
import errno
import os
import subprocess
import sys


def scp(connect_params):
    server_info = connect_params
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        connection.connect(server_info['ip'],
                           username=server_info['sys_user'],
                           password=server_info['sys_pass'],
                           port=server_info['port'],
                           key_filename=server_info['key_filename'],
                           )

        sftp = connection.open_sftp()
        sftp.get(server_info['compress_file'], server_info['compress_file'])
        sftp.close()
        connection.close()
        return True
        # print "%s connect Success and scp %s success!" % (server_info['ip'], server_info['compress_file'])
    except paramiko.SSHException:
        print "%s connect Failed!" % server_info['ip']
        # return False
        quit()


def makedir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def extract(server_info):
    compress_file = server_info['compress_file']
    deploy_path = server_info['deploy_path']
    if not os.path.exists(deploy_path):
        makedir_p(deploy_path)
    command = 'unzip -o %s -d %s' % (compress_file, deploy_path)
    if command_process(command):
        return True
    else:
        return False


def command_process(command):
    shell_command = '%s' % command
    try:
        subprocess.check_output(shell_command, stderr=subprocess.STDOUT, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False


def check_md5sum(server_info):
    remote_md5sum = servers['md5sum']
    command = 'md5sum %s' % server_info['compress_file']
    try:
        stdout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        md5sum = stdout.strip('\n').split(' ')[0]   # for linux
        if md5sum == remote_md5sum:
            check = True
            return check
    except subprocess.CalledProcessError:
        return False


def symlink_release(server_info):
    if not os.path.exists('/data/wwwroot'):
        makedir_p('/data/wwwroot')
    command = 'if test -L %s; then rm -rf %s && ln -s  %s %s && ls -al %s ;else ln -s  %s %s && ls -al %s;fi' \
              % (server_info['release_path'], server_info['release_path'], server_info['deploy_path'],
                 server_info['release_path'], server_info['release_path'], server_info['deploy_path'],
                 server_info['release_path'], server_info['release_path'])
    try:
        stdout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        print stdout
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == '__main__':
    servers = {}
    if len(sys.argv) != 9:
        print 'Usage %s { ip sys_user sys_pass source_path deploy_path release_path compress_file md5sum }' % \
              sys.argv[0]
        sys.exit(1)
    servers['ip'] = sys.argv[1]
    servers['sys_user'] = sys.argv[2]
    servers['sys_pass'] = sys.argv[3]
    servers['source_path'] = sys.argv[4]
    servers['deploy_path'] = sys.argv[5]
    servers['release_path'] = sys.argv[6]
    servers['compress_file'] = sys.argv[7]
    servers['md5sum'] = sys.argv[8]
    servers['key_filename'] = None
    servers['port'] = 22
    if not os.path.exists(servers['source_path']):
        makedir_p(servers['source_path'])
    if check_md5sum(servers):
        # print "already Latest!"
        if extract(servers):
            if not symlink_release(servers):
                print "symlink Failed"
        else:
            print "Extract Failed"
    else:
        if scp(servers):
            if check_md5sum(servers):
                if extract(servers):
                    symlink_release(servers)