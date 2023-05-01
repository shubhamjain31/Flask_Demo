from celery import shared_task

from core.database import models
from core.database.connection import session

from wsgi import app


@shared_task(name="test_beat")
def test_beat():
    with app.app_context():
        pass
        
    print('New Data Updated!')
    return
