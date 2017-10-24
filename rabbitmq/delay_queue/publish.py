# encoding: utf-8
import pika

'''创建rabbitmq连接'''
credentials = pika.PlainCredentials("michael","michael")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.12.171',credentials=credentials))

'''创建channel与发送者confirm'''
channel = connection.channel()
channel.confirm_delivery()
'''声明正常的队列'''
channel.queue_declare(queue='hello', durable=True)
channel.queue_bind(exchange='amq.direct',
                   queue='hello')

delay_channel = connection.channel()
delay_channel.confirm_delivery()


delay_channel.queue_declare(queue='hello_delay', durable=True,  arguments={
  'x-message-ttl' : 60000,
  'x-dead-letter-exchange' : 'amq.direct',
  'x-dead-letter-routing-key' : 'hello'
})

delay_channel.basic_publish(exchange='',
                      routing_key='hello_delay',
                      body="test",
                      properties=pika.BasicProperties(delivery_mode=2))

print " [x] Sent"