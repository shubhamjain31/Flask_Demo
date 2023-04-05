from flask import Blueprint, render_template, jsonify

from core.database.models import User
from core.schemas.model_schema import user_schema, users_schema
from core.database.connection import session
from app.services import user

blueprint = Blueprint("auth", __name__, url_prefix="/api")
print('weiyweu')

@blueprint.route("/users", methods=["GET"])
def users():
    # all_users = session.query(User).all()
    # return users_schema.dump(all_users)
    data = user.get_multiple(db=db)


@blueprint.route("/")
def root():
    return render_template('index.html')