from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Table, Reservation
from .forms import ReservationForm


def tables_list(request):
    """
    Контроллер для отображения списка всех столиков кафе.
    """
    # 1. Читаем из адресной строки параметр фильтрации 'seats' (например, ?seats=4)
    seats_filter = request.GET.get('seats')

    # 2. Если пользователь ввел число в фильтр, отсекаем ненужные столики
    if seats_filter:
        tables = Table.objects.filter(seats=seats_filter)
    else:
        # Если фильтр пустой, берем абсолютно все столики из базы данных
        tables = Table.objects.all()

    # 3. Передаем список столиков в HTML-шаблон tables_list.html
    return render(request, 'bookings/tables_list.html', {'tables': tables})


@login_required
def create_reservation(request):
    """
    Контроллер для создания новой брони столика.
    Декоратор @login_required не пустит сюда неавторизованных гостей.
    """
    if request.method == 'POST':
        # Если пользователь нажал кнопку отправки формы, собираем присланные данные
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Дополнительное задание: проверяем количество броней пользователя на эту дату
            chosen_date = form.cleaned_data.get('date')
            user_today_reservations = Reservation.objects.filter(
                user=request.user,
                date=chosen_date
            ).count()

            # Если у пользователя уже есть 3 или более броней на этот день, выдаем ошибку
            if user_today_reservations >= 3:
                form.add_error(None, "Вы не можете забронировать более 3 столиков на один день.")
            else:
                # Если всё отлично, привязываем авторизованного пользователя к брони и сохраняем
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.save()
                return redirect('my_reservations')
    else:
        # Если пользователь только открыл страницу, подставляем ID столика из ссылки
        initial_table = request.GET.get('table_id')
        form = ReservationForm(initial={'table': initial_table})

    return render(request, 'bookings/reservation_form.html', {'form': form})


@login_required
def my_reservations(request):
    """
    Контроллер для отображения личного кабинета со списком броней текущего пользователя.
    """
    # Ищем в базе только те бронирования, которые принадлежат залогиненному пользователю
    # .order_by('-date') сортирует список от самых свежих к старым
    reservations = Reservation.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bookings/my_reservations.html', {'reservations': reservations})


from django.shortcuts import render

# Create your views here.
