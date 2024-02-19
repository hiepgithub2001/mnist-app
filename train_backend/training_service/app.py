import json
import pika
from dotenv import load_dotenv
import os
import logging
from dto.training_job_dto import SubmitTrainingJob

from service.training.trainer import Trainer
from service.logging.log import RMQLogger

load_dotenv()
TRAINING_TOPIC = os.getenv("TRAINING_KEY")
TRAINING_JOB_KEY = os.getenv("TRAINING_JOB_KEY")
TRAINING_LOG_KEY = os.getenv("TRAINING_LOGGING_KEY")
MQ_HOST = os.getenv("MQ_HOST")

logging.basicConfig(level=logging.INFO)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=MQ_HOST))
channel = connection.channel()

RMQLogger.createInstance(connection, channel, TRAINING_LOG_KEY)

channel.exchange_declare(exchange=TRAINING_TOPIC, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
    exchange=TRAINING_TOPIC, 
    queue=queue_name, 
    routing_key=TRAINING_JOB_KEY
)


print(' [*] Waiting for logs. To exit press CTRL+C')
def callback(ch, method, properties, body):
    json_data = json.loads(body)
    training_data = SubmitTrainingJob.model_validate(json_data)

    trainer = Trainer(
        training_data.paramter_id, 
        training_data.user_decoded_code, 
        training_data.paramter
    )

    trainer.train_model()

channel.basic_consume(
    queue=queue_name, 
    on_message_callback=callback, 
    auto_ack=True
)

channel.basic_qos(prefetch_count=2)
channel.start_consuming()
