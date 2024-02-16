from models import db, MnistJob
import random


def execute_mnist_job(id):
    mnist_jobs = MnistJob.query.get(id)

    mnist_jobs.status = "RUNNING"

    db.session.commit()

    mnist_jobs.result = dict(
        numX=random.randint(0, 100),
        numY=random.randint(0, 100),
        numZ=random.randint(0, 100)
    )

    mnist_jobs.status = "DONE"

    db.session.commit()
