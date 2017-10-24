import etcd

client = etcd.Client(host='10.69.33.29', port=2379, allow_reconnect=True)
try:
    client.delete("/www.michael.com/node1", recursive=True, dir=True)
except Exception,e:
    print e