import etcd


# client = etcd.Client(host=(('10.69.33.111', 2379), ('10.69.33.112', 2379), ('10.69.33.113', 2379)))
client = client = etcd.Client(host='10.69.33.113', port=2379, allow_reconnect=True)
try:
    r = client.read("/registry/services/endpoints/default/www-michael-com", recursive=True)
    k8sService = eval(r.value)
    sipList = k8sService["subsets"][0]["addresses"]
    for ip in sipList:
        print ip["ip"]
    print k8sService["subsets"][0]["ports"][0]["port"]

#    for child in r.children:
#       print "Key:"+ child.key + " " + "Value:" + child.value

except Exception, e:
    print e