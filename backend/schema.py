from marshmallow import fields, Schema


class MnistJobSchema(Schema):
    id = fields.Integer(dump_only=True)
    config = fields.Dict(required=True)
    result = fields.Dict(required=True)
    logs = fields.Raw(required=True)
