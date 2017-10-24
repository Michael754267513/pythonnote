# encoding: utf-8
import pika

'''创建rabbitmq连接'''
credentials = pika.PlainCredentials("michael","michael")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.2.188',credentials=credentials))
channel = connection.channel()

'''设置消息以及匹配routingkey'''
routing_key = ["task_queue", "hello", "michael"]

'''遍历消息以及routingkey'''
for message in range(1, 400):
    channel.basic_publish(exchange='test',
                          routing_key="task_queue",
                          body=str(message),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # 持久化消息
                          ))
    '''打印发送消息'''
    print "Sent Message:%s" % (message,)

'''关闭连接'''
connection.close()