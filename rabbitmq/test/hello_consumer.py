# encoding: utf-8
import pika

rabbitmq_user = "michael"
rabbitmq_passwd = "michael"
rabbitmq_host = "192.168.2.188"

'''创建连接'''
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_passwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=rabbitmq_host, credentials=credentials))
channel = connection.channel()

print ' [*] Waiting for messages. To exit press CTRL+C'

'''回调和ack'''
def callback(ch, method, properties, body):
    print "%s - %s - %s - %s" % (ch, method, properties, body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

'''设置qos,防止大量unack'''
channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback,
                      queue='test')
'''启动消费者'''
channel.start_consuming()