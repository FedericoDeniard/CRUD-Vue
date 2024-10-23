from marshmallow import Schema, fields

class UserPreferencesSchema(Schema):
    timezone = fields.Str(required=True)

class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    roles = fields.List(fields.Str(), required=True)
    preferences = fields.Nested(UserPreferencesSchema, required=True)
    active = fields.Boolean(required=True)
    created_ts = fields.Float(required=True)
