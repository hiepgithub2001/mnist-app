import base64

from flask import Flask, request, jsonify
from config.message_queue import RabbitMQPublisher

from model.model import db
from config.database import DATABASE_URL

from service.job_service import JobService
from repositories.model_repo import MLModelRepository
from repositories.mnist_job_repo import MnistJobRepository

from dto.submit_training_job_request import SubmitTrainingJob
from dto.submit_parameter_req import SubmitParamter

import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

logging.basicConfig(level=logging.INFO)

def init_mq_publisher():
    return RabbitMQPublisher()

def init_database():
    db.init_app(app)
    db.create_all()

@app.route('/submit_code', methods=['POST'])
def submit_code():
    try:
        request_data = SubmitTrainingJob.model_validate(request.json)

        user_decoded_code = base64.b64decode(request_data.user_code_encoded).decode()
        hyper_param = request_data.hyper_parameter

        job_service.submit_job(user_decoded_code, hyper_param)

        return jsonify({'message': 'User code submitted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        init_database()

        mq_publiser = init_mq_publisher()

        job_repo = MnistJobRepository(db)
        model_repo = MLModelRepository(db)

        job_service = JobService(
            model_repo=model_repo,
            job_repo=job_repo,
            mq_publisher=mq_publiser
        )

        app.run(debug=True)
