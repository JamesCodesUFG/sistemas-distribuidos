import pika, threading
import base64
import json

def decode_msg(data: bytes):
    _json = json.loads(data)

    return {key: (base64.b64decode(value) if key == "file" else value) for key, value in _json.items()}

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
            self.__callback(decode_msg(body.decode()))

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
            self.__callback(decode_msg(body.decode()))

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

def encode_msg(data: dict):
    _base64 = {key: (base64.b64encode(value).decode('utf-8') if isinstance(value, bytes) else value) for key, value in data.items()}

    return json.dumps(_base64)

def rabbit_single_send(queue: str, message: dict, host: str = 'localhost'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='', routing_key=queue, body=encode_msg(message))

    connection.close()

def rabbit_multiple_send(exchange: str, message: dict, host: str = 'localhost'):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=host))

    channel = conn.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    channel.basic_publish(exchange=exchange, routing_key='', body=encode_msg(message))

    conn.close()

