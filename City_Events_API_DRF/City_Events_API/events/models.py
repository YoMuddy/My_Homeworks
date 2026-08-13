from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Кастомная модель пользователя, расширяющая стандартный класс AbstractUser.
    Добавлено управление подпиской на уведомления и валидация почты.
    """
    # Флаг для управления рассылками (позволяет пользователю отключать уведомления)
    notify = models.BooleanField(default=True)

    # Поле email делается обязательным и уникальным для корректной работы почтового сервиса
    email = models.EmailField(unique=True)

    # Переопределяем встроенное поле групп, задавая ему уникальное имя 'custom_user_groups'
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )

    # Переопределяем встроенное поле разрешений, задавая ему уникальное имя 'custom_user_permissions'
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

class Event(models.Model):
    """
    Модель для хранения информации о городских мероприятиях и встречах.
    """
    name = models.CharField(max_length=255)  # Название события
    meeting_time = models.DateTimeField()  # Дата и время проведения встречи
    description = models.TextField()  # Детальное описание

    # Связь "Многие-ко-многим" для фиксации участников, записавшихся на событие
    users = models.ManyToManyField(User, related_name='events', blank=True)

    # Служебные флаги для предотвращения повторной отправки уведомлений в фоновых задачах.
    # Предотвращают дублирование писем при циклическом запуске планировщика.
    reminded_1_day = models.BooleanField(default=False)
    reminded_6_hours = models.BooleanField(default=False)

    def __str__(self):
        return self.name
