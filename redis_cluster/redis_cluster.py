from rediscluster import StrictRedisCluster
from redis_cluster_monitor_key import *
'''
    redis cluster node info
'''

'''
    redis-py-cluster
'''

rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
redis_cluster_info = rc.cluster_info()
redis_nodes_info = rc.info()
redis_nodes_config = rc.config_get()

'''
        redis ip and port
'''

monitor_redis_node = "192.168.12.171:6379"
monitor_key = "used_memory"
DBsize = ["dbsize", "keys", "cluster_size"]

if monitor_key in  redis_nodes_config[monitor_redis_node]:
    print redis_nodes_config[monitor_key]
elif monitor_key in monitor_cluster_key:
    print str(redis_cluster_info[monitor_redis_node][monitor_key])
elif monitor_key in DBsize:
    print rc.dbsize()[monitor_redis_node]
else:
    try:
            print redis_nodes_info[monitor_redis_node][monitor_key]
    except:
            print monitor_key + " is not found"

print rc.client_getname()
#print redis_nodes_config["192.168.12.172:6379"]
#print  redis_nodes_info["192.168.12.172:6379"]
#for k in redis_cluster_info:
#    print redis_cluster_info[k]
#    print k +" " + str(redis_cluster_info[k]["cluster_size"])