
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.env import POSTGERSS_DB, POSTGRESS_PASSWORD, POSTGRESS_PORT, POSTGRESS_HOST, POSTGRESS_USER

DATABASE_URL = f'postgresql+psycopg2://{POSTGRESS_USER}:{POSTGRESS_PASSWORD}@{POSTGRESS_HOST}:{POSTGRESS_PORT}/{POSTGERSS_DB}'