from flask import Blueprint, render_template

from core.database.models import User
# from core.schemas.model_schema import user_schema, users_schema

blueprint = Blueprint("auth", __name__, url_prefix="/api")
print('weiyweu')

# @blueprint.route("/users", methods=["GET"])
# def users():
#     all_users = User.all()
#     return users_schema.dump(all_users)


@blueprint.route("/")
def root():
    return render_template('index.html')