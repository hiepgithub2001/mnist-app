from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from models import MLModel, MnistJob, JobLogging, JobStatus


class JobLoggingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = JobLogging
        load_instance = True  # Optional: deserialize to model instances


class JobStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = JobStatus
        load_instance = True  # Optional: deserialize to model instances


class MLModelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MLModel
        load_instance = True  # Optional: deserialize to model instances


class MnistJobSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MnistJob
        load_instance = True  # Optional: deserialize to model instances

    related_status = fields.Nested(JobStatusSchema)
    related_logs = fields.Nested(JobLoggingSchema, many=True)
    related_ml_model = fields.Nested(MLModelSchema, only=('id', 'name'))
