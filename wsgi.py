from main import get_application
from flask import jsonify

from decouple import config
from utils.helper import ValidationException
from core.database.admin import admin_panel
from core.database.models import User

import flask_login as login


login_manager = login.LoginManager()

app     = get_application()
admin   = admin_panel(app)

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.errorhandler(ValidationException)
def handle_validation_exception(exc):
    return (
        jsonify({"msssage": exc.msssage, "status": exc.status_code, "data": exc.data}),
        exc.status_code,
    )

if __name__ == '__main__':
    app.run(debug=config("DEBUG"))