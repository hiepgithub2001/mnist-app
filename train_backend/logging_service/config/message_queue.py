# rabbitmq.py
import pika

from config.env import TRAINING_TOPIC, TRAINING_LOG_KEY, MQ_HOST

class RabbitMQConsumer:
    def __init__(self, queue_name, callback):
        self.queue_name = queue_name
        self.callback = callback

    def start_consuming(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_HOST))
        channel = connection.channel()

        channel.exchange_declare(exchange=TRAINING_TOPIC, exchange_type='topic')
        channel.queue_declare(queue=self.queue_name, exclusive=True)

        channel.queue_bind(
            exchange=TRAINING_TOPIC,
            queue=self.queue_name,
            routing_key=TRAINING_LOG_KEY
        )

        channel.basic_consume(
            queue=self.queue_name, 
            on_message_callback=self.callback, 
            auto_ack=True
        )

        print(f'Consumer for queue {self.queue_name} started. Waiting for messages...')
        channel.start_consuming()

class RabbitMQPublisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_HOST))
        self.channel = self.connection.channel()

    def publish_message(self, exchange_name, routing_key, message):
        self.channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
        print(f" [x] Sent '{message}' to '{routing_key}'")

    def close_connection(self):
        self.connection.close()

        
