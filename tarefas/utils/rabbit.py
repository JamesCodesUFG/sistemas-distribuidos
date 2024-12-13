import pika, threading
import json

class RabbitSingleReceiver(threading.Thread):
    def __init__(self, host: str, queue: str, callback):
        super().__init__(daemon=True)

        self.__conn = pika.BlockingConnection(pika.ConnectionParameters(host=host))

        self.__queue = queue
        self.__callback = callback


    def run(self):
        channel = self.__conn.channel()

        channel.queue_declare(queue=self.__queue)

        def callback(ch, method, properties, body):
            self.__callback(json.dumbs(body))

        channel.basic_consume(queue=self.__queue, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

class RabbitMultipleReceiver(threading.Thread):
    def __init__(self, host: str, exchange: str, callback):
        super().__init__(daemon=True)

        self.__conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.__exchange = exchange
        self.__callback = callback

    def run(self):
        channel = self.__conn.channel()

        channel.exchange_declare(exchange=self.__exchange, exchange_type='fanout')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=self.__exchange, queue=queue_name)

        def callback(ch, method, properties, body):
            self.__callback(json.dumbs(body))

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

def rabbit_send(queue: str, message: str | bytes):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='', routing_key=queue, body=message)

    connection.close()

def rabbit_multiple_send(exchange: str, message: str | bytes, host: str = 'localhost'):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=host))

    channel = conn.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    channel.basic_publish(exchange='logs', routing_key='', body=message)

    conn.close()