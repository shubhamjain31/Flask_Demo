from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from decouple import config

from config import settings

import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core/templates')
static_dir   = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core/static')

def get_application() -> Flask:
    app = Flask(__name__, template_folder=template_dir, static_url_path="", static_folder=static_dir)
    
    app.secret_key = config("SECRET_KEY")

    if config('ENVIRONMENT') == "production":
        app.config.from_pyfile('config/production.py')

    elif config('ENVIRONMENT') == "development":
        app.config.from_pyfile('config/development.py')

    else:
        app.config.from_pyfile('config/local.py')

    CORS(app, support_credentials=True)

    return app

app     = get_application()

if __name__ == '__main__':
    app.run(debug=config("DEBUG"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def method_not_allowed(e):
    return render_template("500.html"), 500


@app.route("/")
@cross_origin(supports_credentials=True)
def root():
    return render_template('index.html')