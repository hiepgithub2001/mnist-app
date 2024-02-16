from functools import wraps
from flask import jsonify, request, Blueprint, session
from marshmallow import ValidationError
from models import db, MnistJob
from schema import MnistJobSchema


app = Blueprint('mnist_job', __name__)

mnist_schema = MnistJobSchema()


def validate_with(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                data = schema.load(request.json)
            except ValidationError as err:
                return jsonify(err.messages), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/get', methods=['GET'])
def get_mnist_jobs():
    records = MnistJob.query.all()
    return jsonify([mnist_schema.dump(record) for record in records])


@app.route('/add', methods=['POST'])
def add_mnist_jobs():
    config = request.json['config']

    mnist_jobs = MnistJob(config)
    db.session.add(mnist_jobs)
    db.session.commit()

    return mnist_schema.dump(mnist_jobs)


@app.route('/update/<id>', methods=['PUT'])
def update_mnist_job(id):
    mnist_job = MnistJob.query.get(id)
    config = request.json['config']

    mnist_job.config = config

    db.session.commit()
    return mnist_schema.dump(mnist_job)


@app.route('/delete/<id>', methods=['DELETE'])
def delete_mnist_job(id):
    mnist_job = MnistJob.query.get(id)

    if not mnist_job:
        return jsonify({
            "Status": "The mnist_job is not exist!"
        })

    db.session.delete(mnist_job)
    db.session.commit()
    return mnist_schema.dump(mnist_job)
