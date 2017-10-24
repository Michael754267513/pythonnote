from pykafka import KafkaClient
client = KafkaClient(
                     ## zookeeper_hosts="192.168.2.200:2181,192.168.2.228:2181,192.168.2.204:2181"
zookeeper_hosts="127.0.0.1:2181"
                     )
topic = client.topics["test"]
consumer = topic.get_simple_consumer(consumer_group="Michael")
for message in consumer:
    if message is not None:
        print message.offset, message.value