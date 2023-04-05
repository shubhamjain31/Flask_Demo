from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow

from decouple import config

from config import settings
from app.api import blueprint

import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core/templates')
static_dir   = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core/static')

app = Flask(__name__)

def get_application() -> Flask:
    
    # flask app initiate
    app = Flask(__name__, 
                template_folder=template_dir, 
                static_url_path="", 
                static_folder=static_dir)
    
    # secret key
    app.secret_key = config("SECRET_KEY")

    app.register_blueprint(blueprint)

    # postgressql URL
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL

    # loading environment variable
    if config('ENVIRONMENT') == "production":
        app.config.from_pyfile('config/production.py')

    elif config('ENVIRONMENT') == "development":
        app.config.from_pyfile('config/development.py')

    else:
        app.config.from_pyfile('config/local.py')

    # bypass cors header
    CORS(app, support_credentials=True, resources={r"/*": {"origins": settings.ALLOWED_ORIGINS}})

    return app


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def method_not_allowed(e):
    return render_template("500.html"), 500


# @app.route("/")
# @cross_origin(supports_credentials=True)
# def root():
#     return render_template('index.html')

# from core.database.models import User
# class UserSchema(Serializer.Schema):

#     class Meta:
#         model = User
#         ordered = True
#         load_instance = True
#         fields = ("username", "email", "name", "password", "is_active", "profile", "date_created")


# user_schema = UserSchema()
# users_schema = UserSchema(many=True)

# @app.route("/users", methods=["GET"])
# def users():
#     all_users = User.all()
#     return users_schema.dump(all_users)