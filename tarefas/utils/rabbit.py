import pika, threading

class RabbitReceiver(threading.Thread):
    def __init__(self, queue: str, callback):
        super().__init__(daemon=True)

        self.__queue = queue
        self.__callback = callback


    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        channel = connection.channel()

        channel.queue_declare(queue=self.__queue)

        def callback(ch, method, properties, body):
            self.__callback(body)

        channel.basic_consume(queue=self.__queue, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

def rabbit_send(queue: str, body: str | bytes):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='', routing_key=queue, body=body)

    connection.close()