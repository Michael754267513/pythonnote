# encoding: utf-8
import pika, time

'''创建rabbitmq连接'''
credentials = pika.PlainCredentials("michael", "michael")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.12.171', credentials=credentials))


delay_channel = connection.channel()
'''发送消息确认'''
delay_channel.confirm_delivery()

'''消息延迟时间(ms)'''
headers = {
    "x-delay": 10000
}
delay_channel.basic_publish(exchange='delay',
                      routing_key='delay',
                      body=str( time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))),
                      properties=pika.BasicProperties(headers=headers, delivery_mode=2))

print " [x] Sent"