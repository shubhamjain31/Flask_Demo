from core.database.models import User

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
    def change_none_to_string(cls, data, **kwargs):
        # fields = cls.fields
        # print(fields)
        # field_map = {
        #     "str": "",
        #     "int": 0,
        #     "float": 0.0,
        #     "list": [],
        #     "dict": {},
        #     "bool": False,
        #     "datetime": ""
        # }

        # field_type = {}

        # for field in fields.items():
        #     field_type.update({field[0]: field[1]._bind_to_schema.__name__})

        # print(field_type)

        # for key, value in data.items():

        #     try:
        #         if not value:
        #             data[key] = field_map[field_type[key]]
        #     except KeyError:
        #         pass
        # return data
        for field in data:
            if data[field] is None:
                data[field] = ""
        return data


user_schema = UserSchema()
users_schema = UserSchema(many=True)