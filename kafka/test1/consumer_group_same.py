from pykafka import KafkaClient
client = KafkaClient(
                     zookeeper_hosts="192.168.2.200:2181,192.168.2.228:2181,192.168.2.204:2181"
                     )
topic = client.topics["kafka.consume"]
balance_consumer = topic.get_balanced_consumer(consumer_group="kafka",
                           zookeeper_connect="192.168.2.200:2181,192.168.2.228:2181,192.168.2.204:2181",
                           auto_commit_enable=True
                                          )
for message in balance_consumer:
    if message is not None:
        print message.offset, message.value