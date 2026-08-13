from django.apps import AppConfig

class EventsConfig(AppConfig):
    """
    Конфигурационный класс для управления приложением events.
    Используется для настройки системы и автоматической регистрации сигналов при старте.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

    def ready(self):
        # Инициализируем и подключаем файл сигналов.
        # Это гарантирует, что обработчики событий (рассылка писем при создании ивента)
        # успешно зарегистрируются в системе в момент запуска веб-сервера.
        import events.signals
