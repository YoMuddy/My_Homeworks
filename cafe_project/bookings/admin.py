from django.contrib import admin
from .models import Table, Reservation

# Регистрируем модель столиков
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    # Какие колонки показывать в таблице списка столиков
    list_display = ('number', 'seats')
    # По какому полю будет работать строка поиска
    search_fields = ('number',)

# Регистрируем модель бронирований
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # Колонки для списка броней
    list_display = ('table', 'user', 'date', 'hour_start', 'hour_end', 'created_at')
    # Боковой фильтр по датам и столикам
    list_filter = ('date', 'table')


# Register your models here.
