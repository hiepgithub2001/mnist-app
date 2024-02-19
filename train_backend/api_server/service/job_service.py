from config.message_queue import RabbitMQPublisher
from dto.submit_parameter_req import HyperParametersDTO

from repositories.mnist_job_repo import MnistJobRepository
from repositories.model_repo import MLModelRepository

from model.model import db

import base64
import hashlib
import json


class JobService:
    def __init__(self, 
        model_repo : MLModelRepository, 
        job_repo : MnistJobRepository, 
        mq_publisher : RabbitMQPublisher
    ):
        self.model_repo = model_repo
        self.job_repo = job_repo
        self.publisher = mq_publisher
    
    def run_job(self, model_srcipt : str, mnist_job_config : HyperParametersDTO, mnist_job_id : int):
            message = {
                'user_decoded_code' : model_srcipt,
                'paramter_id' : mnist_job_id,
                'paramter' : mnist_job_config.tojson()
            }

            self.publisher.publish_job(json.dumps(message))