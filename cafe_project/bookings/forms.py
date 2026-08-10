from django import forms
from datetime import date
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'hour_start', 'hour_end']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        reservation_date = cleaned_data.get('date')
        hour_start = cleaned_data.get('hour_start')
        hour_end = cleaned_data.get('hour_end')

        if not all([table, reservation_date, hour_start, hour_end]):
            return cleaned_data

        # Проверка рабочих часов кафе (с 8:00 до 18:00)
        if hour_start < 8 or hour_end > 18:
            raise forms.ValidationError("Кафе работает только с 8:00 до 18:00.")
        if hour_start >= hour_end:
            raise forms.ValidationError("Время начала не может быть больше или равно времени окончания.")

        # Проверка, что дата не в прошлом
        if reservation_date < date.today():
            raise forms.ValidationError("Нельзя забронировать столик на прошлую дату.")

        # Проверка на пересечение бронирований
        overlapping_reservations = Reservation.objects.filter(
            table=table,
            date=reservation_date,
            hour_start__lt=hour_end,
            hour_end__gt=hour_start
        )
        if overlapping_reservations.exists():
            raise forms.ValidationError("Этот столик уже занят на выбранное время.")

        return cleaned_data
