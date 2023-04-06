from flask import Blueprint, render_template, request

from core.database.models import User
from core.schemas.model_schema import user_schema, users_schema
from core.database.connection import session
from app.service import user

from utils.helper import APIResponse

from sqlalchemy.orm import Session

blueprint = Blueprint("auth", __name__, url_prefix="/api")

@blueprint.route("/users", methods=["GET"])
def users():
    # all_users = session.query(User).all()
    # return users_schema.dump(all_users)
    data = user.get_multiple(db=session)
    return data

@blueprint.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    print(data,'iii')
    data = user.create(db=session, user=data)
    return APIResponse(data, status_code=201, message='User Added!')