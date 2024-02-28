from functools import wraps
import json
from flask import jsonify, request, Blueprint, session, current_app
from marshmallow import ValidationError
from service.job_service import JobService
from dto.submit_parameter_req import HyperParametersDTO
from model.model import db, MnistJob, MLModel, JobLogging, JobStatus
from model.schema import MnistJobSchema, MLModelSchema
import hashlib


job_controller = Blueprint('mnist_job', __name__)

mnist_schema = MnistJobSchema()
ml_model_schema = MLModelSchema()

def execute_mnist_job(model_id, config, config_id):
    model : MLModel = MLModel.query.filter_by(id=model_id).first()

    if model is None:
        raise Exception(f"model with id = {model_id} is not exist in database")

    try:
        print(config)
        config_dto = HyperParametersDTO.model_validate(config)
        with current_app.app_context():
            job_service : JobService = current_app.config["JOB_SERVICE"]
            job_service.run_job(
                model_srcipt=model.model_script,
                mnist_job_config=config_dto,
                mnist_job_id=config_id
            )
    except Exception as e:
        raise e

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


@job_controller.route('/submit_ml_model', methods=['POST'])
def summit_ml_model():
    name = request.json['name']
    model_script = request.json['model_script']

    md5_hash = get_MD5_hash(model_script)

    if MLModel.query.filter_by(hash = md5_hash).first() is not None:
        return jsonify(json.dumps({"error" : "Duplicate Model"})), 409

    model = MLModel(
        name=name, 
        model_script=model_script, 
        hash=get_MD5_hash(model_script)
    )

    db.session.add(model)
    db.session.commit()

    return jsonify(ml_model_schema.dump(model)), 200


@job_controller.route('/get_ml_model', methods=['GET'])
def get_ml_model():
    models = MLModel.query.all()
    return jsonify([ml_model_schema.dump(item) for item in models])


@job_controller.route('/get_mnist_job', methods=['POST'])
def get_mnist_jobs():
    list_status = request.json['list_status']

    if not list_status:
        list_status = []

    mnist_job_ids = JobStatus.query.filter(JobStatus.status.in_(list_status)).all()

    list_id = [item.mnist_job_id for item in mnist_job_ids]

    print(list_id)

    records = MnistJob.query.filter(MnistJob.id.in_(list_id)).all()

    return jsonify([mnist_schema.dump(record) for record in records])


@job_controller.route('/add_mnist_job', methods=['POST'])
def add_mnist_jobs():
    ml_model_id = request.json['ml_model_id']
    config = request.json['config']

    mnist_jobs = MnistJob(model_id=ml_model_id, config=config, result=None)
    db.session.add(mnist_jobs)
    db.session.commit()

    try:
        execute_mnist_job(ml_model_id, mnist_jobs.config, mnist_jobs.id)
        return mnist_schema.dump(mnist_jobs)
    except Exception as e:
        return jsonify({ "error" : str(e) }), 500


@job_controller.route('/retry_mnist_job/<id>', methods=['POST'])
def retry_mnist_job(id):
    mnist_job : MnistJob = MnistJob.query.get(id)

    if mnist_job.related_status:
        mnist_job.related_status.status = "PENDING"
        db.session.commit()

    model_id = mnist_job.related_ml_model

    try:
        execute_mnist_job(model_id, mnist_job.config, mnist_job.id)
        return mnist_schema.dump(mnist_job)
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

@job_controller.route('/update_mnist_job/<id>', methods=['PUT'])
def update_mnist_job(id):
    mnist_job = MnistJob.query.get(id)
    config = request.json['config']

    mnist_job.config = config

    db.session.commit()
    return mnist_schema.dump(mnist_job)


@job_controller.route('/delete_mnist_job/<id>', methods=['DELETE'])
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

def get_MD5_hash(user_decoded_code : str):
    md5 = hashlib.md5()
    md5.update(user_decoded_code.encode())

    return md5.hexdigest()