from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # ID should not be user-provided
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    
class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    due_date = fields.DateTime(required=True)
    priority = fields.Str(required=True, validate=validate.OneOf(["low", "medium", "high"]))
    status = fields.Str(validate=validate.OneOf(["incomplete", "complete"]))
    user_id = fields.Int(required=True)
