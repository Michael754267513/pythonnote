import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.2.188', credentials=pika.PlainCredentials("michael","michael")))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):
    #n = int(body)

    print(" [.] fib(%s)" % body)
    response = "ipconfig"

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()