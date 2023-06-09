from core.database.models import User, Post

from flask_marshmallow import Marshmallow
from marshmallow import post_dump

Serializer = Marshmallow()

class UserSchema(Serializer.Schema):

    class Meta:
        model = User
        ordered = True
        load_instance = True
        fields = ("id", "username", "email", "name", "password", "is_active", "profile", "date_created")

    @post_dump
    def change_none_values(cls, data, **kwargs):
        fields = cls.Meta.model.__dict__.get('__table__').columns
        
        field_map = {
            "VARCHAR": "",
            "INTEGER": 0,
            "FLOAT": 0.0,
            "JSON": {},
            "BOOLEAN": False,
            "DATETIME": ""
        }

        field_type = {}

        for field in fields:
            type_ = str(field.type).split("(")
            field_type.update({field.name: type_[0]})

        for key, value in data.items():

            try:
                if not value:
                    data[key] = field_map[field_type[key]]
            except KeyError:
                pass
        return data
    
class PostSchema(Serializer.Schema):

    class Meta:
        model = Post
        ordered = True
        load_instance = True
        fields = ("id", "post_name", "post_text", "user_id", "created_at", "updated_at")

    @post_dump
    def change_none_values(cls, data, **kwargs):
        fields = cls.Meta.model.__dict__.get('__table__').columns
        
        field_map = {
            "VARCHAR": "",
            "INTEGER": 0,
            "FLOAT": 0.0,
            "JSON": {},
            "BOOLEAN": False,
            "DATETIME": ""
        }

        field_type = {}

        for field in fields:
            type_ = str(field.type).split("(")
            field_type.update({field.name: type_[0]})

        for key, value in data.items():

            try:
                if not value:
                    data[key] = field_map[field_type[key]]
            except KeyError:
                pass
        return data

user_schema  = UserSchema()
users_schema = UserSchema(many=True)

post_schema  = PostSchema()
posts_schema = PostSchema(many=True)