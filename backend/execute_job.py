from models import db, MnistJob, JobStatus, JobLogging
import random


def execute_mnist_job(mnist_job_id):
    print("Execute mnist job with id: ", mnist_job_id)
    mnist_jobs = MnistJob.query.get(mnist_job_id)

    if mnist_jobs.related_status:
        mnist_jobs.related_status.status = "RUNNING"
    else:
        new_status = JobStatus()
        new_status.status = "RUNNING"

        mnist_jobs.related_status = new_status

        db.session.add(new_status)

    if mnist_jobs.related_logs:
        mnist_jobs.related_logs.batching += 12
    else:
        new_log = JobLogging()
        new_log.batching = 12

        mnist_jobs.related_logs = new_log

        db.session.add(new_log)

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

    mnist_jobs.related_logs.content = "The progress is Done"
    mnist_jobs.related_status.status = "DONE"
    db.session.commit()
