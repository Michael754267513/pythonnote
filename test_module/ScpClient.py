#encoding: utf-8
from paramiko import SSHClient

ssh = SSHClient()
ssh.connect("192.168.2.188",22,"root","Xujiahui@123",key_filename="G:\code\config\ssh_key")
scp = SSHClient(ssh.get_transport())
local_file="G:\code\config\hosts"
remote_file="/tmp/ddddd"
scp.put(local_file,remote_file)
scp.close()
