from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

# Define a sample task
@celery.task
def add(x, y):
    return x + y