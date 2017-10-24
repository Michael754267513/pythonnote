from kafka import KafkaProducer

client = KafkaProducer(zookeeper_hosts="192.168.2.200:2181,192.168.2.228:2181,192.168.2.204:2181")

client.send("www", "aaaaaaa")