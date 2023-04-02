from decouple import config

if config('ENVIRONMENT') == "production":
    from .production import *
elif config('ENVIRONMENT') == "development":
    from .development import *
else:
    from .local import *