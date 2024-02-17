from models import db, MnistJob, JobStatus
from schema import JobStatusSchema
import random


def execute_mnist_job(id):
    mnist_jobs = MnistJob.query.get(id)

    if mnist_jobs.related_status:
        mnist_jobs.related_status.status = "RUNNING"
        db.session.commit()
    else:
        new_status = JobStatus()
        new_status.status = "RUNNING"

        mnist_jobs.related_status = new_status

        db.session.add(new_status)
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

    mnist_jobs.related_status.status = "DONE"
    db.session.commit()
