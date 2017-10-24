import etcd

client = etcd.Client(host='10.69.33.113', port=2379, allow_reconnect=True)

try:
    r = client.read("/upstreams", recursive=True)
    for child in r.children:
        print "Key:"+ child.key + " " + "Value:" + child.value

except Exception, e:
    print e