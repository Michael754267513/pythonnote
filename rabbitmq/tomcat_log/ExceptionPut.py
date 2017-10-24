import pika

'''创建一个连接'''
credentials = pika.PlainCredentials("michael","michael")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.2.188',credentials=credentials))
channel = connection.channel()

print(' [*] Waiting for logs. To exit press CTRL+C')
'''回调'''
def callback(ch, method, properties, body):
    print body

channel.basic_consume(callback,
                      queue="Exception",
                      no_ack=True)
'''开启消费'''
channel.start_consuming()