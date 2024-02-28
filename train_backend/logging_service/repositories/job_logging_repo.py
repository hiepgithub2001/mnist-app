from flask_sqlalchemy import SQLAlchemy
from model.model import JobLogging

class JobLoggingRepository:
    def __init__(self, db : SQLAlchemy):
        self.db = db

    def create(self, mnist_job_id: int, batching: int, content: str):
        job_logging = JobLogging(mnist_job_id=mnist_job_id, batching=batching, content=content)
        self.db.session.add(job_logging)
        self.db.session.commit()
        return job_logging

    def get_by_id(self, job_logging_id: int):
        return self.db.session.query(JobLogging).filter(JobLogging.id == job_logging_id).first()

    def update(self, job_logging_id: int, batching: int, content: str):
        job_logging = self.get_by_id(job_logging_id)
        if job_logging:
            job_logging.batching = batching
            job_logging.content = content
            self.db.session.commit()
            return job_logging
        return None

    def delete(self, job_logging_id: int):
        job_logging = self.get_by_id(job_logging_id)
        if job_logging:
            self.db.session.delete(job_logging)
            self.db.session.commit()
            return True
        return False
