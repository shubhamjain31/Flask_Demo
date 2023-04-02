from decouple import config


if config('ENVIRONMENT') == "production":
    from .production import *
elif config('ENVIRONMENT') == "development":
    from .development import *
else:
    from .local import *

class Settings(object):
    
    SECRET_KEY: str     = config("SECRET_KEY")
    PROJECT_NAME: str   = config("PROJECT_NAME")
    API_V1_STR: str     = config("API_V1_STR")

settings = Settings()