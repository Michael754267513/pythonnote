from pykafka import KafkaClient
import time
client = KafkaClient(
                    zookeeper_hosts="127.0.0.1:2181"
                     )
topic = client.topics["test1"]
with topic.get_sync_producer() as producer:
    for i in range(100):
        time.sleep(1)
        message = "kafka: " + str(i)
        producer.produce(message)