# rabbitmq.py
import pika
from config.env import TRAINING_TOPIC, TRAINING_TOPIC, MQ_HOST, TRAINING_JOB_KEY

class RabbitMQPublisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_HOST))
        self.channel = self.connection.channel()

    def publish_message(self, exchange_name, routing_key, message):
        self.channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
        print(f" [x] Sent '{message}' to '{routing_key}'")
    
    def publish_job(self, message):
        self.channel.basic_publish(exchange=TRAINING_TOPIC, routing_key=TRAINING_JOB_KEY, body=message)
        print(f" [x] Sent '{message}' to '{TRAINING_JOB_KEY}'")

    def close_connection(self):
        self.connection.close()

        
