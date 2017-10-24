import etcd

client = etcd.Client(host='10.69.33.29', port=2379, allow_reconnect=True)

check = '{"weight":1, "max_fails":1, "fail_timeout":10}'
client.write("/upstreams/test/1.1.1.5:80", check, ttl=None)

try:
    r = client.read("/upstreams/test/", recursive=True)
    for child in r.children:
        print "Key:"+ child.key + " " + "Value:" + child.value

except Exception, e:
    print e
