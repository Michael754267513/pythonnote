from pykafka import KafkaClient
from pykafka.simpleconsumer import  OffsetType
client = KafkaClient(
                      zookeeper_hosts="127.0.0.1:2181"
                     )
topic = client.topics["test1"]
consumer = topic.get_simple_consumer(consumer_group="Michael",
                                     auto_offset_reset=OffsetType.EARLIEST,
                                     reset_offset_on_start=True
                                     )
for message in consumer:
    if message is not None:
        print message.offset, message.value