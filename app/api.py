from flask import Blueprint, request

from core.database.connection import session
from app.service import user, authenticate

from utils.decorators import token_required
from utils.helper import send_email

blueprint = Blueprint("auth", __name__, url_prefix="/api")

@blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = authenticate.login(user=data, tbl=session)
    return {"status":200, "message":'Login Successfully!', "data": response}, 200

@blueprint.route("/users", methods=["GET"])
@token_required
def users(current_user):
    # all_users = session.query(User).all()
    # return users_schema.dump(all_users)
    response = user.get_multiple(tbl=session)
    return {"status":200, "message":'All User!', "data": response}, 200

@blueprint.route("/user/<userId>", methods=["GET"])
@token_required
def user_(current_user, userId: str):
    response = user.get(id=userId, tbl=session)
    # send_email()
    return {"status":200, "message":'Specific User!', "data": response}, 200

@blueprint.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    response = user.create(tbl=session, user=data, ip_address=request.remote_addr, user_agent=request.headers.get('User-Agent'))

    template = """
        <html>
        <body>
         
        <p>Hi !!!
        <br>Thanks for the registration!!!</p>
 
        </body>
        </html>
        """
    message = ""
    send_email(message, template, "Welcome TO Demo", [response['email']])
    return {"status":201, "message":'User Added!', "data": response}, 201

@blueprint.route("/edit-user/<userId>", methods=["PUT"])
@token_required
def edit_user(current_user, userId: str):
    data = request.form.to_dict()
    response = user.update(id=userId, tbl=session, user=data, media=request.files)
    return {"status":200, "message":'User Updated!', "data": response}, 200

@blueprint.route("/delete-user/<userId>", methods=["DELETE"])
@token_required
def delete_user(current_user, userId: str):
    response = user.delete(id=userId, tbl=session)
    return {"status":200, "message":'User Deleted!', "data": response}, 200

@blueprint.route("/change-password/<userId>", methods=["PATCH"])
@token_required
def password_change(current_user, userId: str):
    data = request.get_json()
    response = user.change_password(user=data, id=userId,  tbl=session)
    return {"status":200, "message":'Password Changed!', "data": response}, 200
