from flask_sqlalchemy import SQLAlchemy
from model.model import MnistJob


class MnistJobRepository:
    def __init__(self, db : SQLAlchemy):
        self.db = db

    def get_model_config_by_id(self, job_id):
        return self.db.session.query(MnistJob).filter(MnistJob.id == job_id).first()

    def create_model_config(self, model_id, config, result):
        model_config = MnistJob(model_id=model_id, config=config, result=result)
                                        
        self.db.session.add(model_config)
        self.db.session.commit()
        return model_config

    def update_model_config(self, job_id, config=None, result=None):
        mnist_job = self.db.session.query(MnistJob).filter(MnistJob.id == job_id).first()
        if mnist_job:
            if config is not None:
                mnist_job.config = config
            if result is not None:
                mnist_job.result = result
        self.db.session.commit()

        return mnist_job
    
    def delete_model_config(self, job_id):
        model_config = self.db.session.query(MnistJob).filter(MnistJob.id == job_id).first()
        if model_config:
            self.db.session.delete(model_config)
            self.db.session.commit()