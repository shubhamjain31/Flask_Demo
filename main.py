from flask import Flask, render_template
from flask_cors import CORS, cross_origin

from decouple import config

from config import settings
from app.api import blueprint

from utils.helper import APIResponse, mail

from celery import Celery
from celery.schedules import crontab

import os

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['app.tasks']
)

celery.conf.beat_schedule = {
    'load_data_at_10': {
        'task': 'test_beat',
        'schedule': crontab(minute='*/1')
    }
}

celery.conf.timezone = 'Asia/Kolkata'

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

    app.config.update(
        MAIL_SERVER         = settings.MAIL_SERVER,
        MAIL_PORT           = settings.MAIL_PORT,
        MAIL_USE_TLS        = True,
        MAIL_USERNAME       = settings.MAIL_USERNAME,
        MAIL_PASSWORD       = settings.MAIL_PASSWORD
    )

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

    mail.init_app(app)

    return app

@blueprint.route("/")
@cross_origin(supports_credentials=True)
def root():
    return render_template('index.html')