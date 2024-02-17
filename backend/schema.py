from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import MLModel, MnistJob, JobLogging, JobStatus


class MLModelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MLModel
        load_instance = True  # Optional: deserialize to model instances


class MnistJobSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MnistJob
        load_instance = True  # Optional: deserialize to model instances


class JobLoggingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = JobLogging
        load_instance = True  # Optional: deserialize to model instances


class JobStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = JobStatus
        load_instance = True  # Optional: deserialize to model instances
