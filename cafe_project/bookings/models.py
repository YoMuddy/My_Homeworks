from django.db import models
# Импортируем стандартную модель пользователя, которая уже есть в Django
from django.contrib.auth.models import User


class Table(models.Model):
    # Номер столика. IntegerField — это поле для целых чисел.
    # unique=True проверяет, чтобы в базе не появилось двух столиков с одинаковым номером.
    number = models.IntegerField(unique=True, verbose_name="Номер столика")

    # Поле для картинки. Все загруженные фото будут складываться в папку 'tables/'.
    image = models.ImageField(upload_to='tables/', verbose_name="Изображение столика")

    # Количество мест за столиком. Тоже целое число.
    seats = models.IntegerField(verbose_name="Количество мест")

    # Метод __str__ говорит Django, как отображать этот объект в виде текста (например, в админке)
    def __str__(self):
        return f"Столик №{self.number} ({self.seats} мест)"


class Reservation(models.Model):
    # Связываем бронь со столиком. models.CASCADE означает: если удалить столик из базы,
    # то автоматически удалятся и все связанные с ним бронирования.
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name="Столик")

    # Связываем бронь с пользователем, который её сделал.
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    # Поле для даты (день, месяц, год).
    date = models.DateField(verbose_name="Дата бронирования")

    # Время начала и конца брони храним простыми целыми числами (например, 8, 9, 14, 18).
    hour_start = models.IntegerField(verbose_name="Час начала")
    hour_end = models.IntegerField(verbose_name="Час окончания")

    # Дата и время создания самой записи. auto_now_add=True автоматически ставит текущее время при сохранении.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def __str__(self):
        return f"Бронь столика №{self.table.number} ({self.user.username})"

from django.db import models

# Create your models here.
