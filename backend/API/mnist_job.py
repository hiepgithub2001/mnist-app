from functools import wraps
from flask import jsonify, request, Blueprint, session
from marshmallow import ValidationError
from models import db, MnistJob, MLModel, JobLogging, JobStatus
from schema import MnistJobSchema
from execute_job import execute_mnist_job


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


@app.route('/get_mnist_job', methods=['POST'])
def get_mnist_jobs():
    list_status = request.json['list_status']

    if not list_status:
        list_status = []

    mnist_job_ids = JobStatus.query.filter(JobStatus.status.in_(list_status)).all()

    list_id = [item.mnist_job_id for item in mnist_job_ids]

    print(list_id)

    records = MnistJob.query.filter(MnistJob.id.in_(list_id)).all()

    return jsonify([mnist_schema.dump(record) for record in records])


@app.route('/add_mnist_job', methods=['POST'])
def add_mnist_jobs():
    config = request.json['config']

    mnist_jobs = MnistJob(config)
    db.session.add(mnist_jobs)
    db.session.commit()

    execute_mnist_job(mnist_jobs.id)

    return mnist_schema.dump(mnist_jobs)


@app.route('/retry_mnist_job/<id>', methods=['POST'])
def retry_mnist_job(id):
    mnist_jobs = MnistJob.query.get(id)
    mnist_jobs.status = "PENDING"
    db.session.add(mnist_jobs)
    db.session.commit()

    execute_mnist_job(mnist_jobs.id)

    return mnist_schema.dump(mnist_jobs)


@app.route('/update_mnist_job/<id>', methods=['PUT'])
def update_mnist_job(id):
    mnist_job = MnistJob.query.get(id)
    config = request.json['config']

    mnist_job.config = config

    db.session.commit()
    return mnist_schema.dump(mnist_job)


@app.route('/delete_mnist_job/<id>', methods=['DELETE'])
def delete_mnist_job(id):
    mnist_job = MnistJob.query.get(id)

    if not mnist_job:
        return jsonify({
            "Status": "The mnist_job is not exist!"
        })

    db.session.delete(mnist_job)
    db.session.commit()
    return mnist_schema.dump(mnist_job)
