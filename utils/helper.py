import random
from flask import Response, jsonify

class ValidationException(Exception):
    def __init__(self, data, status_code, msssage):
        self.data = data
        self.status_code = status_code
        self.msssage = msssage

def generate_username(name):
    first_letter = name[0][0]
    three_letters_surname = name[-1][:3]
    number = '{:03d}'.format(random.randrange(1, 999))
    username = (first_letter + three_letters_surname + number)
    return username

class APIResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(APIResponse, cls).force_type(rv, environ)