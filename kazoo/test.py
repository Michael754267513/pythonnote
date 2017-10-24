from kazoo.client import KazooClient
import logging
logging.basicConfig()

zk = KazooClient(hosts="192.168.12.236:2181,192.168.12.237:2181,192.168.12.238:2181")
zk.start()
#print zk.client_id
#print zk.hosts
#print zk.state
#print zk.Barrier
zk_list = zk.get_children("/dubbo")
zk_list = list(set(zk_list))
no_comsumer= []
for value in zk_list:
     api = "/dubbo/%s" % value
     if zk.get_children(api).__len__() <= 2:
        #print value
        #print zk.get_children(api)
        no_comsumer.append(value)
print "no consumers list: %s" % no_comsumer.__len__()
print zk.get_children("/dubbo/com.xjh.api.service.PayServiceApi")
    #print zk.get_children(value)


zk.stop()