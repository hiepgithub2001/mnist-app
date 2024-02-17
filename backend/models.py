from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
import hashlib

db = SQLAlchemy()


def hash_script_md5(script_code):
    # Create an MD5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the script code string
    md5_hash.update(script_code.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_script_md5 = md5_hash.hexdigest()

    return hashed_script_md5


# class MnistJob(db.Model):
#     __tableame__ = 'mnist_job'
#     id = db.Column(db.Integer, primary_key=True)
#     config = db.Column(db.JSON)
#     result = db.Column(db.JSON)
#     logs = db.Column(db.JSON)
#     status = db.Column(db.String(256), default="PENDING")

#     def __init__(self, config):
#         self.config = config


class MLModel(db.Model):
    _tablename_ = 'ml_model'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256), unique=True, nullable=False)
    model_script = db.Column(db.Text)
    hash = db.Column(db.Text)

    def __init__(self, name, model_script):
        self.name = name
        self.model_script = model_script
        self.hash = hash_script_md5(model_script)


class MnistJob(db.Model):
    _tablename_ = 'mnist_job'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer,  db.ForeignKey('ml_model.id'))

    config = db.Column(db.JSON)
    result = db.Column(db.JSON)

    related_status = db.relationship("JobStatus", backref="mnist_job", uselist=False)
    related_logs = db.relationship("JobLogging", backref="mnist_job", uselist=False)
    related_ml_model = db.relationship('MLModel')

    def __init__(self, ml_model_id, config):
        self.model_id = ml_model_id
        self.config = config


class JobLogging(db.Model):
    _tablename_ = 'job_logging'
    id = db.Column(db.Integer, primary_key=True)
    mnist_job_id = db.Column(db.Integer,  db.ForeignKey('mnist_job.id'), unique=True)

    batching = db.Column(db.Integer)
    content = db.Column(db.TEXT)


class JobStatus(db.Model):
    _tablename_ = 'job_status'
    id = db.Column(db.Integer, primary_key=True)
    mnist_job_id = db.Column(db.Integer,  db.ForeignKey('mnist_job.id'), unique=True)

    status = db.Column(db.String(256), default="PENDING")
    current_epoch = db.Column(db.Integer)
    progress = db.Column(db.Integer)
    loss = db.Column(db.Float)
