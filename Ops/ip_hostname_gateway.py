# encoding: utf-8
import re
import sys
'''
    修改ip与hostname格式: eth0 192.168.1.111/24 192.168.1.1 www.example.com
'''
WK_file = "/etc/sysconfig/network-scripts/ifcfg-%s" % sys.argv[1]
HN_file = "/etc/sysconfig/network"
NW = sys.argv[1]
network = sys.argv[2].split("/")[1]
ip = sys.argv[2].split("/")[0]
gateway = sys.argv[3]
hostname = sys.argv[4]
print '''
    主机名:   %s
    网卡:     %s
    ip地址:   %s
    掩码:     %s
    网关:     %s
''' % (hostname, NW, ip, network, gateway)
