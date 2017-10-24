# encoding: utf-8
import pika, time

'''创建rabbitmq连接'''
credentials = pika.PlainCredentials("michael","michael")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.2.188',credentials=credentials))
channel = connection.channel()

print ' [*] Waiting for messages. To exit press CTRL+C'

'''标记回调,以及设置fail消息'''
def callback(ch, method, properties, body):
    if body == "task_queue":
        '''设置消费失败的routingkey'''
        method.routing_key = "task_queue.fail"
        '''使用nack来标记消息失败'''
        #ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        '''使用reject来标记消息失败'''
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        '''打印失败的消息'''
        print "message fail: %s" % body
    else:
        '''消费消息回复ack'''
        print " 发送消息时间: %r -- 当前时间:%s" % (body,str( time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))))
        ch.basic_ack(delivery_tag=method.delivery_tag)

'''设置qos'''
channel.basic_qos(prefetch_count=1)
'''绑定队列'''
channel.basic_consume(callback,
                      exchange='delay')
'''启动消费者'''
channel.start_consuming()