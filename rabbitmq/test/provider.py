# encoding: utf-8
import pika, sys

rabbitmq_user = "michael"
rabbitmq_passwd = "michael"
rabbitmq_host = "192.168.2.188"

'''创建连接'''
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_passwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=rabbitmq_host, credentials=credentials))
channel = connection.channel()

message="asdada"
channel.basic_publish(exchange='',  #设置交换机
                          routing_key="test", #设置routingkey
                          body=str(message), #设置发送消息
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # 持久化消息
                          ))

'''打印发送消息'''
print "Sent Message:%s" % (message)

'''关闭连接'''
connection.close()