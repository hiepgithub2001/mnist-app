from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def get_uuid():
    return uuid4().hex


class MnistJob(db.Model):
    __tableame__ = 'mnist_job'
    id = db.Column(db.Integer, primary_key=True)
    config = db.Column(db.JSON)
    result = db.Column(db.JSON)
    logs = db.Column(db.JSON)
    status = db.Column(db.String(256), default="pending")

    def __init__(self, config):
        self.config = config
