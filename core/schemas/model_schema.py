from core.database.models import User

from flask_marshmallow import Marshmallow

Serializer = Marshmallow()

class UserSchema(Serializer.Schema):

    class Meta:
        model = User
        ordered = True
        load_instance = True
        fields = ("id", "username", "email", "name", "password", "is_active", "profile", "date_created")


user_schema = UserSchema()
users_schema = UserSchema(many=True)