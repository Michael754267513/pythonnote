import etcd

client = etcd.Client(host='10.69.33.29', port=2379, allow_reconnect=True)

client.write('/www.michael.com/node1', "1.1.1.1")
client.write('/www.michael.com/node4', "1.1.1.2")
client.write('/www.michael.com/node2', "2.2.2.2")
client.write('/www.michael.com/node3', "3.3.3.3")
