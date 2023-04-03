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

settings = Settings()