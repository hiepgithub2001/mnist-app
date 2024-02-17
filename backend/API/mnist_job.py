from functools import wraps
from flask import jsonify, request, Blueprint, session
from marshmallow import ValidationError
from models import db, MnistJob, MLModel, JobLogging, JobStatus
from schema import MnistJobSchema, MLModelSchema
from execute_job import execute_mnist_job


app = Blueprint('mnist_job', __name__)

mnist_schema = MnistJobSchema()
ml_model_schema = MLModelSchema()


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


@app.route('/submit_ml_model', methods=['POST'])
def summit_ml_model():
    name = request.json['name']
    model_script = request.json['model_script']
    model = MLModel(name, model_script)
    db.session.add(model)
    db.session.commit()
    return jsonify(ml_model_schema.dump(model))


@app.route('/get_ml_model', methods=['GET'])
def get_ml_model():
    models = MLModel.query.all()
    return jsonify([ml_model_schema.dump(item) for item in models])


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
    ml_model_id = request.json['ml_model_id']
    config = request.json['config']

    mnist_jobs = MnistJob(ml_model_id, config)
    db.session.add(mnist_jobs)
    db.session.commit()

    execute_mnist_job(mnist_jobs.id)

    return mnist_schema.dump(mnist_jobs)


@app.route('/retry_mnist_job/<id>', methods=['POST'])
def retry_mnist_job(id):
    mnist_job = MnistJob.query.get(id)

    if mnist_job.related_status:
        mnist_job.related_status.status = "PENDING"
        db.session.commit()

    execute_mnist_job(id)

    return mnist_schema.dump(mnist_job)


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
        return jsonify({"Status": "The mnist_job does not exist!"}), 404

    if mnist_job.related_status:
        db.session.delete(mnist_job.related_status)

    if mnist_job.related_logs:
        db.session.delete(mnist_job.related_logs)

    db.session.delete(mnist_job)
    db.session.commit()

    return jsonify({"Status": "MnistJob deleted successfully"}), 200
