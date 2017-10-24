import pika
import time

credentials = pika.PlainCredentials("michael","michael")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.2.188',credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True,)
print ' [*] Waiting for messages. To exit press CTRL+C'


def callback(ch, method, properties, body):
    if body == "task_queue":
        ch.basic_reject(requeue=False)

    else:
        print " [x] Received %r" % (body,)
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()