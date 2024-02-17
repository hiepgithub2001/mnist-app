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

    # Just test with other schema
    if (mnist_jobs.result['numX'] % 2 == 0):
        mnist_jobs.result = dict(
            numA=random.randint(0, 100),
            numB=random.randint(0, 100),
            numC=random.randint(0, 100)
        )

    mnist_jobs.status = "DONE"

    db.session.commit()
