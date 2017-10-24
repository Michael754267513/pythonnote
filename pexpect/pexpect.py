import pexpect, getpass, os,time

#!/bin/env python

import pexpect,getpass,os,time

ask_ssh = 'Are you sure you want to continue connecting'
conn_time = 'Connection timed out'
ok_ssh = 'ssh/authorized_keys'
child = pexpect.spawn('ssh-copy-id -i /%s/.ssh/id_rsa.pub %s@%s' % ("root","root","192.168.12.174"))
res = child.expect([pexpect.TIMEOUT, ask_ssh, 'password: ',conn_time,ok_ssh])
if res == 0:
        print "time out!"
        child.close()
elif res == 1:
        #print child.before, child.after
        child.sendline ('yes')
        child.expect('password:')
        child.sendline('Xujiahui@123')
        time.sleep(3)
        child.close()
elif res == 2:
        child.sendline('Xujiahui@123')
        time.sleep(3)
        child.close()
elif res == 3:
        print "failed"
else:
        #print child.before, child.after
        print "key is ok"
        child.close()