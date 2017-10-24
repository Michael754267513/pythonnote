import redis

ip = "192.168.12.171"
port = "6379"
password = ""
db = 0
redis_conn = redis.StrictRedis(host=ip, port=port, db=db,password=password)
print redis_conn.client_list()
print  redis_conn.ping()
print  redis_conn.config_get('maxmemory')
print  redis_conn.dbsize()
info_list = redis_conn.info()
print info_list
print  info_list["tcp_port"]
print info_list["slave0"]["ip"]
if "tcp_1port" in info_list:
    print "11111"
else:
        print "22222"
        redis_conn = redis.StrictRedis(host=ip, port=port, db=db, password=password)
        info_list = redis_conn.info()

