from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from flask import session


db = SQLAlchemy()


def get_uuid():
    return uuid4().hex


class MnistJob(db.Model):
    __tableame__ = 'mnist_job'
    id = db.Column(db.Integer, primary_key=True)
    config = db.Column(db.JSON)
    result = db.Column(db.JSON)
    logs = db.Column(db.JSON)

    def __init__(self, config):
        self.config = config
