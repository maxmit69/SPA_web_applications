import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Настройка параметров брокера
app.conf.update(
    broker_url='redis://localhost:6379/0',  # URL для подключения к брокеру
    broker_connection_retry_on_startup=True,  # Повторное подключение к брокеру
)
