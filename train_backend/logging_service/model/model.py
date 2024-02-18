from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

db = SQLAlchemy()
class MLModel(db.Model):
    _tablename_ = 'ml_model'
    id = db.Column(db.Integer, primary_key=True)

    model_script = db.Column(db.Text)
    hash = db.Column(db.Text)

    related_mnist_job = db.relationship('MnistJob', backref='ml_model')


class MnistJob(db.Model):
    _tablename_ = 'mnist_job'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer,  db.ForeignKey('ml_model.id'))

    config = db.Column(db.JSON)
    result = db.Column(db.JSON)

    related_status = db.relationship("JobStatus", backref="mnist_job", uselist=False)
    related_logs = db.relationship("JobLogging", backref="mnist_job")


class JobLogging(db.Model):
    _tablename_ = 'job_logging'
    id = db.Column(db.Integer, primary_key=True)
    mnist_job_id = db.Column(db.Integer,  db.ForeignKey('mnist_job.id'))

    batching = db.Column(db.Integer)
    content = db.Column(db.String)


class JobStatus(db.Model):
    _tablename_ = 'job_status'
    id = db.Column(db.Integer, primary_key=True)
    mnist_job_id = db.Column(db.Integer,  db.ForeignKey('mnist_job.id'))

    status = db.Column(db.String(256), default="PENDING")
    current_epoch = db.Column(db.Integer)
    progress = db.Column(db.Integer)
    loss = db.Column(db.Float)