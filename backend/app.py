from flask import Flask
from flask_cors import CORS, cross_origin
from models import db
from config import ApplicationConfig


# Create a Flask application
app = Flask(__name__,)
app.config.from_object(ApplicationConfig)
CORS(app, supports_credentials=True)


db.init_app(app)

with app.app_context():
    db.create_all()


# Import and register routes
from API.mnist_job import app as mnist_job


app.register_blueprint(mnist_job)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
