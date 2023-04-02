from decouple import config


class Settings(object):
    
    SECRET_KEY: str     = config("SECRET_KEY")
    PROJECT_NAME: str   = config("PROJECT_NAME")
    API_V1_STR: str     = config("API_V1_STR")
    DEBUG: str          = config("DEBUG")

settings = Settings()