from marshmallow import Schema, fields, validate, post_load
from models import *
from models.models import Wall


class WallSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    datetime = fields.Date()
    title = fields.Str()
    text = fields.Str()
    photo_wall = fields.Bool()

    @post_load
    def all_news(self, data, **kwargs):
        return Wall(**data)