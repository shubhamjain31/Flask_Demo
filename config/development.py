from decouple import config


class Settings(object):
    
    SECRET_KEY: str         = config("SECRET_KEY")
    PROJECT_NAME: str       = config("PROJECT_NAME")
    API_V1_STR: str         = config("API_V1_STR")
    DEBUG: str              = config("DEBUG")
    DATABASE_PORT           = 5432
    POSTGRES_PASSWORD       = ""
    POSTGRES_USER           = ""
    POSTGRES_DB             = ""
    POSTGRES_HOST           = ""
    SITE_URL                = ""
    POSTGRES_HOSTNAME       = ""
    DATABASE_URL            = ""
    ALLOWED_ORIGINS         = []
    MAIL_PORT               = 587
    MAIL_SERVER             = "smtp.gmail.com"
    MAIL_FROM_NAME          = "Demo"
    ALGORITHM               = "HS256"
    API_USER_EMAIL          = []
    MAIL_USERNAME: str      = ""
    MAIL_PASSWORD: str      = ""
    MAIL_FROM: str          = ""
    CELERY_BROKER_URL       = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND   = 'redis://localhost:6379'

settings = Settings()