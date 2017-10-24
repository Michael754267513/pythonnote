from pykafka import KafkaClient
client = KafkaClient(
                      zookeeper_hosts="127.0.0.1:2181"
                     )
topic = client.topics["test1"]
consumer = topic.get_simple_consumer(consumer_group="Michael",
                                     )
print  consumer.held_offsets
for message in consumer:
    if message is not None:
        print message.offset, message.value
        consumer.commit_offsets()