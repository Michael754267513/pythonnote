import pika

conn = pika.BaseConnection(pika.ConnectionParameters('192.168.2.230'))
channel = conn.channel()
channel.queue_declare(queue="michael_test",arguments=pika.BasicProperties())


def callback(ch, method, properties, body):
    if body == "michael":

        #channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False

        channel.queue_declare(queue="dead")
    print '''%s - %s - %s - %s''' % (ch, method, properties, body)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='michael_test')
channel.basic_nack(delivery_tag="false",requeue=True)
channel.basic_reject()
channel.start_consuming()
channel.close()
