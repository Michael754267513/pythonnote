from Test_Paramiko import *
from ReadHost import ReadHost

def exec_command(selection,username,password,command):
    for name in ReadHost().get_pc_section(selection):
        ip = ReadHost().get_pc_items(selection)[ReadHost().get_pc_section(selection).index(name)][1]
        sshd = ssh_connect(ip, username, password)
        stdin, stdout, stderr = ssh_exec_cmd(sshd, command)
        err_list = stderr.readlines()
        if len(err_list) > 0:
            print 'ERROR:' + err_list[0]
            exit()
        for item in stdout.readlines():
            print item,
            ssh_close(sshd)