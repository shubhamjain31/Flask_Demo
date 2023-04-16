from flask import Blueprint, request

from core.database.connection import session
from app.service import user

from utils.decorators import token_required

blueprint = Blueprint("auth", __name__, url_prefix="/api")

@blueprint.route('/login', methods=['GET'])
def login():
    return 'welcome %s' % 'name'

@blueprint.route("/users", methods=["GET"])
@token_required
def users():
    # all_users = session.query(User).all()
    # return users_schema.dump(all_users)
    response = user.get_multiple(db=session)
    return {"status":200, "message":'All User!', "data": response}, 200

@blueprint.route("/user/<userId>", methods=["GET"])
def user_(userId: str):
    response = user.get(id=userId, db=session)
    return {"status":200, "message":'Specific User!', "data": response}, 200

@blueprint.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    response = user.create(db=session, user=data, ip_address=request.remote_addr, user_agent=request.headers.get('User-Agent'))
    return {"status":201, "message":'User Added!', "data": response}, 200

@blueprint.route("/edit-user/<userId>", methods=["PUT"])
def edit_user(userId: str):
    data = request.form.to_dict()
    response = user.update(id=userId, db=session, user=data, media=request.files)
    return {"status":200, "message":'User Updated!', "data": response}, 200

@blueprint.route("/delete-user/<userId>", methods=["DELETE"])
def delete_user(userId: str):
    response = user.delete(id=userId, db=session)
    return {"status":200, "message":'User Deleted!', "data": response}, 200