from rediscluster import StrictRedisCluster

'''
    redis cluster node info
'''
startup_nodes = [
    {"host": "192.168.12.171", "port": "6379"},
    {"host": "192.168.12.171", "port": "6380"},
    {"host": "192.168.12.171", "port": "6381"},
    {"host": "192.168.12.172", "port": "6379"},
    {"host": "192.168.12.172", "port": "6380"},
    {"host": "192.168.12.172", "port": "6381"}
]
'''
    redis cluster info for keys
'''
monitor_cluster_key = [
    'cluster_state',
    'cluster_slots_assigned',
    'cluster_known_nodes',
    'cluster_slots_fail',
    'cluster_stats_messages_received',
    'cluster_size',
    'cluster_current_epoch',
    'cluster_stats_messages_sent',
    'cluster_slots_pfail',
    'cluster_my_epoch',
    'cluster_slots_ok'
]

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

#print redis_nodes_config["192.168.12.172:6379"]
#print  redis_nodes_info["192.168.12.172:6379"]
#for k in redis_cluster_info:
#    print redis_cluster_info[k]
#    print k +" " + str(redis_cluster_info[k]["cluster_size"])