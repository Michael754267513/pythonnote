import redis, time

ip = "192.168.2.216"
port = "6379"
password = ""
db = 0

redis_conn = redis.StrictRedis(host=ip, port=port, db=db,password=password)
for num in range(1, 1200):
    redis_conn.setex(str(num),30,num)
key_list =  redis_conn.keys('*')
for key in  key_list:
    if key == "a":
        continue
    if int(key) > 1000:
        print "key: %s" % key
       # time.sleep(0.1)
        print  redis_conn.get(key)
