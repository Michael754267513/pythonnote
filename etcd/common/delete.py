import etcd

client = etcd.Client(host='10.69.33.113', port=2379, allow_reconnect=True)
try:
    client.delete("/upstreams", recursive=True, dir=True)
except Exception,e:
    print e