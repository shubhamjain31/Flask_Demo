from main import get_application

from decouple import config

app     = get_application()

if __name__ == '__main__':
    app.run(debug=config("DEBUG"))