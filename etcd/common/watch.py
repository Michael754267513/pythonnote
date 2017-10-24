import etcd

client = etcd.Client(host='10.69.33.29', port=2379, allow_reconnect=True)

while True:
    change = client.watch("/registry/services/endpoints/", recursive=True, timeout=None)
    print change.key + " " + change.action