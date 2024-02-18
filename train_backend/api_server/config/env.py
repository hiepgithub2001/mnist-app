import os

from dotenv import load_dotenv
load_dotenv()

POSTGRESS_HOST = os.getenv("POSTGRESS_HOST")
POSTGRESS_PORT = os.getenv("POSTGRESS_PORT")
POSTGRESS_USER = os.getenv("POSTGRESS_USER")
POSTGRESS_PASSWORD = os.getenv("POSTGRESS_PASSWORD")
POSTGERSS_DB = os.getenv("POSTGRESS_DB")

TRAINING_TOPIC = os.getenv("TRAINING_KEY")
TRAINING_LOG_KEY = os.getenv("TRAINING_LOGGING_KEY")
TRAINING_JOB_KEY = os.getenv("TRAINING_JOB_KEY")
MQ_HOST = os.getenv("MQ_HOST")