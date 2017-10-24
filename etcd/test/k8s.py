# encoding=utf-8
import etcd

# 创建etcd连接
client = client = etcd.Client(host='10.69.33.113', port=2379, allow_reconnect=True)

def podslist(namespaces, service):

    iplist = [];
    try:
        # 服务地址相关转化成字典
        r = client.read("/registry/services/endpoints/%s/%s" % (namespaces, service), recursive=True)
        k8sService = eval(r.value)
        # 获取地址端口
        siplist = k8sService["subsets"][0]["addresses"]
        # 获取服务端口
        sport = k8sService["subsets"][0]["ports"][0]["port"]
        # 服务端口和port组成port返回
        for ip in siplist:
            iplist.append(ip["ip"] + ":" + str(sport))
        return iplist
    except Exception, e:
        return e

# namespace 和 服务
namespace = "default"
service = "www-michael-com"

endpoints = podslist(namespace, service)
# nginx check方式
servercheck = '{"weight":1, "max_fails":1, "fail_timeout":10}'
# 添加后端 upstream server
for server in endpoints:

    client.write("/upstreams/%s/%s" % (service, server), servercheck, ttl=None)