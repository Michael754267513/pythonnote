import pika

credentials = pika.PlainCredentials("michael","michael")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.2.188',credentials=credentials))
channel = connection.channel()


result = channel.queue_declare(exclusive=True)
queue_name = "test"

#channel.queue_bind(exchange='logs',
#                  queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=False)
channel.start_consuming()