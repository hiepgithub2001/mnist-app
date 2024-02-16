from marshmallow import fields, Schema


class HyperParamSchema(Schema):
    a = fields.Integer(required=True)
    b = fields.Integer(required=True) 


class MnistJobSchema(Schema):
    id = fields.Integer(dump_only=True)
    config = fields.Nested(HyperParamSchema, required=True)
    result = fields.Raw(required=True)
    logs = fields.Raw(required=True)
