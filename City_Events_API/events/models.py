from django.db import models
# Импортируем встроенную модель пользователя, чтобы связать её с событиями
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=255)  # Название
    meeting_time = models.DateTimeField()  # Дата и время
    description = models.TextField()  # Описание

    # НОВОЕ ПОЛЕ: список участников события.
    # blank=True означает, что изначально на событие никто не подписан (список пустой)
    users = models.ManyToManyField(User, related_name='events', blank=True)

    def __str__(self):
        return self.name
