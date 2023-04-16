import time

import jwt
from decouple import config
from config import settings


JWT_SECRET      = config("SECRET_KEY")
JWT_ALGORITHM   = config("ALGORITHM")


def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str, email: str):
   
    if email in settings.API_USER_EMAIL:
        payload = {
            "user_id": user_id,
            "expires": False       # infinite expiration time
        }
    else:
        payload = {
            "user_id": user_id,
            "expires": time.time() + 3600       # expire in one hour
        }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"] is False:
            return decoded_token
        else:
            return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}