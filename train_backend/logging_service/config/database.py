import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.env import DB_NAME, DB_PASSWORD, DB_PORT, DB_HOST, DB_USER

DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'