from functools import wraps

from core.database.models import User, Token

from flask import request

from decouple import config
from core.database.connection import session
from app.authentication import decodeJWT

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        # return 401 if token is not passed
        if not token:
            return {"status":401, "message":'Invalid Token !!', "data": {}}, 401
  
        try:
            check_token = session.query(Token).filter_by(token = token).first()
            if check_token is None:
                return {"status":401, "message":'Token is invalid !!', "data": {}}, 401
            
            # decoding the payload to fetch the stored details
            data = decodeJWT(token)
            current_user = session.query(User).filter_by(id = data['user_id']).first()

            if current_user is None:
                return {
                    "status":401,
                    "message": "Invalid Authentication token!",
                    "data": None
                }, 401
        except Exception as e:
            return {"status":401, "message":'Token is invalid !!', "data": {}}, 401
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated