from flask import Blueprint, render_template, request

from core.database.connection import session
from app.service import user

blueprint = Blueprint("auth", __name__, url_prefix="/api")

@blueprint.route("/users", methods=["GET"])
def users():
    # all_users = session.query(User).all()
    # return users_schema.dump(all_users)
    response = user.get_multiple(db=session)
    return {"status":200, "message":'All User!', "data": response}

@blueprint.route("/user/<userId>", methods=["GET"])
def user_(userId: str):
    response = user.get(id=userId, db=session)
    return {"status":200, "message":'Specific User!', "data": response}

@blueprint.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    response = user.create(db=session, user=data, ip_address=request.remote_addr, user_agent=request.headers.get('User-Agent'))
    return {"status":201, "message":'User Added!', "data": response}

@blueprint.route("/edit-user/<userId>", methods=["PUT"])
def edit_user(userId: str):
    data = request.form.to_dict()
    response = user.update(id=userId, db=session, user=data, media=request.files)
    return {"status":200, "message":'User Updated!', "data": response}
