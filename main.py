from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

from decouple import config

from config import settings
from app.api import blueprint

from utils.helper import APIResponse

import os, flask_login

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core/templates')
static_dir   = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core/static')

def page_not_found(e):
    return render_template("404.html"), 404

def internal_server_error(e):
    return render_template("500.html"), 500

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

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    app.response_class = APIResponse

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    return app

@blueprint.route("/")
@cross_origin(supports_credentials=True)
def root():
    return render_template('index.html')