import os

from dotenv import load_dotenv
load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

TRAINING_TOPIC = os.getenv("TRAINING_KEY")
TRAINING_LOG_KEY = os.getenv("TRAINING_LOGGING_KEY")
MQ_HOST = os.getenv("MQ_HOST")