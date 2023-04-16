from functools import wraps

from core.database.models import User

import jwt

from flask import request, jsonify

from decouple import config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return {"status":401, "message":'Token is missing !!!', "data": {}}, 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(email = data['email'])\
                .first()
        except:
            return {"status":401, "message":'Token is invalid !!', "data": {}}, 401
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated