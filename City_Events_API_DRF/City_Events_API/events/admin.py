from django.contrib import admin
from .models import Event

# Говорим Django показывать таблицу событий в панели управления
admin.site.register(Event)
