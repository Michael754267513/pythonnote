#!/bin/env python
import pexpect, time, sys, os, ConfigParser

def check_public_key(localuser):
    path = "/%s/.ssh/id_rsa.pub" % localuser
    if os.path.exists(path):
            pass
    else:
            print "please check local %s  id_rsa.pub" % localuser
            print "maybe you should run ssh-keygen to make this file"
            sys.exit(2)

def sshkey(localuser, remoteuser, remotehost, password, sshport):
    ask_ssh = 'Are you sure you want to continue connecting'
    conn_time = 'Connection timed out'
    ok_ssh = 'ssh/authorized_keys'
    cmd = "ssh-copy-id -i /%s/.ssh/id_rsa.pub '-p %s %s@%s'" % (localuser, sshport, remoteuser, remotehost)
    child = pexpect.spawn(cmd)
    res = child.expect([pexpect.TIMEOUT, ask_ssh, 'password: ', conn_time, ok_ssh])
    if res == 0:
        print "ssh timeout to connection %s" % remotehost
        child.close()
    elif res == 1:
        # print child.before, child.after
        child.sendline('yes')
        res = child.expect(['password: ', ok_ssh])
        if res == 1:
                print "%s ---- success " % remotehost
                child.close()
        else:
                child.sendline(password)
                time.sleep(3)
                child.close()
                print "%s ---- success " % remotehost
    elif res == 2:
        child.sendline(password)
        time.sleep(3)
        child.close()
        print "%s ---- success " % remotehost
    elif res == 3:
        print "connection timed out - host: %s - port: %s" % (remotehost,sshport)
    else:
        # print child.before, child.after
        print "%s ---- success " % remotehost
        child.close()

cf = ConfigParser.ConfigParser()

cf.read("/etc/config/sshkey.conf")
localuser = cf.get("sshkey","localuser")
remoteuser = cf.get("sshkey","remoteuser")
password = cf.get("sshkey","password")
#remotehost = cf.get("sshkey","remotehost")
sshport = cf.get("sshkey","sshport")

file = open("/etc/config/remotehosts")
for remotehost in file:
        sshkey(localuser, remoteuser, remotehost, password, sshport)