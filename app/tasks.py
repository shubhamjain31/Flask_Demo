from celery import shared_task

from core.database import models
from core.database.connection import session

from wsgi import app


@shared_task(name="load_mandi_data")
def load_mandi_data():
    with app.app_context():
        pass
        
    print('New Data Updated!')
    return
