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

    def submit_job(self, user_decoded_code : str, parameter : HyperParametersDTO):
        md5_hash = self.get_MD5_hash(user_decoded_code)

        if self.model_repo.get_model_by_hash(md5_hash) != None:
            raise Exception("Duplicated model")
        else:
            ml_model = self.model_repo.add_model(user_decoded_code, md5_hash)
            parameter_model = self.job_repo.create_model_config(
                model_id=ml_model.id,
                config=json.dumps(parameter.tojson()),
                result=None
            )

            message = {
                'user_decoded_code' : user_decoded_code,
                'paramter_id' : parameter_model.id,
                'paramter' : parameter.tojson()
            }

            self.publisher.publish_job(json.dumps(message))
    
    def submit_param(self, user_model_id : int, parameter : HyperParametersDTO):
        model = self.model_repo.get_model_by_id(user_model_id)

        if model is None:
            return
        
        user_decoded_code = base64.b64decode(model.model_script).decode()
        parameter_model = self.job_repo.create_model_config(
            learning_rate=parameter.lr,
            num_epoch=parameter.epochs,
            batch_size=parameter.batch_size,
            drop_out=parameter.drop_out
        )

        return True
    
    def get_MD5_hash(self, user_decoded_code : str):
        md5 = hashlib.md5()
        md5.update(user_decoded_code.encode())

        return md5.hexdigest()