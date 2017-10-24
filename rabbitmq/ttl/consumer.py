# encoding: utf-8
import pika, time

'''创建rabbitmq连接'''
credentials = pika.PlainCredentials("michael","michael")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.2.188',credentials=credentials))
channel = connection.channel()

print ' [*] Waiting for messages. To exit press CTRL+C'

'''回调和ack'''
def callback(ch, method, properties, body):
    #if body == "a5" or body == "a6":
     #   ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
      #  time.sleep(10)
    #else:
        print "%s - %s - %s - %s" % (ch, method, properties, body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

'''设置qos,防止大量unack'''
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='aaaaa')
'''启动消费者'''
channel.start_consuming()