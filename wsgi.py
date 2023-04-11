from main import get_application
from flask import jsonify

from decouple import config
from utils.helper import ValidationException

app     = get_application()

@app.errorhandler(ValidationException)
def handle_validation_exception(exc):
    return (
        jsonify({"msssage": exc.msssage, "status": exc.status_code, "data": exc.data}),
        exc.status_code,
    )

if __name__ == '__main__':
    app.run(debug=config("DEBUG"))