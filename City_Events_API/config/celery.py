import os
from celery import Celery

# Указываем настройки Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Явно передаем адрес Redis прямо при создании экземпляра Celery (заменяем дефолтный amqp)
app = Celery('config', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')

# Читаем остальные конфигурации (например, маршруты очередей) из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи tasks.py внутри ваших приложений
app.autodiscover_tasks()
