import pika

conn = pika.BaseConnection(pika.ConnectionParameters('192.168.2.230'))
channel = conn.channel(on_open_callback="1",channel_number=1)
channel.queue_declare(queue="michael_test", durable=True, arguments={'x-dead-letter-routing-key': 'dead'})
message = "this is test!"
channel.basic_publish(exchange="", routing_key="test", body=message, properties=pika.BasicProperties(
                         delivery_mode = 2
                      ))
conn.close()
