from decouple import config


class Settings(object):
    
    SECRET_KEY: str         = config("SECRET_KEY")
    PROJECT_NAME: str       = config("PROJECT_NAME")
    API_V1_STR: str         = config("API_V1_STR")
    DEBUG: str              = config("DEBUG")
    DATABASE_PORT           = 5432
    POSTGRES_PASSWORD       = "root"
    POSTGRES_USER           = "postgres"
    POSTGRES_DB             = "flask_demo"
    POSTGRES_HOST           = "localhost"
    SITE_URL                = "http://127.0.0.1:5000"
    POSTGRES_HOSTNAME       = "127.0.0.1"
    DATABASE_URL            = "postgresql+psycopg2://postgres:root@localhost/flask_demo"
    ALLOWED_ORIGINS         = ["localhost", "127.0.0.1"]
    MAIL_PORT               = 587
    MAIL_SERVER             = "smtp.gmail.com"
    MAIL_FROM_NAME          = "Demo"
    ALGORITHM               = "HS256"
    API_USER_EMAIL          = ["admin@email.com"]
    MAIL_USERNAME: str      = config("MAIL_USERNAME")
    MAIL_PASSWORD: str      = config("MAIL_PASSWORD")
    MAIL_FROM: str          = config("MAIL_FROM")
    CELERY_BROKER_URL       = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND   = 'redis://localhost:6379'

settings = Settings()