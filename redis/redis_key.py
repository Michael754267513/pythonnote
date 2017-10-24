#encoding: utf-8
import redis, time

ip = "192.168.2.216"
port = "6379"
password = ""
db = 0

redis_conn = redis.StrictRedis(host=ip, port=port, db=db,password=password)
key_list =  redis_conn.keys('*')

def redis_qps(qps_time):
    info_list = redis_conn.info()
    hits_keys = info_list["keyspace_hits"]
    miss_keys = info_list["keyspace_misses"]
    first_keys = hits_keys + miss_keys
    exp_key = info_list["expired_keys"]
    dbsize = redis_conn.dbsize()
    db0_size = dbsize + exp_key
    time.sleep(int(qps_time))
    info_list1 = redis_conn.info()
    hits_keys1 = info_list1["keyspace_hits"]
    miss_keys1 = info_list1["keyspace_misses"]
    last_keys = hits_keys1 + miss_keys1
    avg_qps = last_keys - first_keys
    exp_key = info_list1["expired_keys"]
    dbsize1 = redis_conn.dbsize()
    db0_size1 = dbsize + exp_key
    avg_dbsize = db0_size1 - db0_size
    print '''
        时间: %s s
        读QPS: %.2f
        写QPS: %.2f
    ''' % (str(qps_time), float(avg_qps)/float(qps_time), float(avg_dbsize)/float(qps_time))
def redis_lagre_key():
    for key in key_list:
        strlen = redis_conn.strlen(key)
        if strlen > 1048576: # 输出大于1MB的key以及长度
            print  '''key: %s  strlen: %s''' % (key, strlen)
def redis_hit_miss():
    info_list = redis_conn.info()
    hits_keys = info_list["keyspace_hits"]
    miss_keys = info_list["keyspace_misses"]
    all_keys = hits_keys + miss_keys
    print "命中率: %.2f%s" %  (float(hits_keys)/all_keys * 100, "%")
redis_qps("10")
redis_lagre_key()
redis_hit_miss()