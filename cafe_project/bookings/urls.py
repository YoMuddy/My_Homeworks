from django.urls import path
from . import views

urlpatterns = [
    # Главная страница со списком столиков (адрес: /tables/)
    path('', views.tables_list, name='tables_list'),


    # Страница создания новой брони (адрес: /reservations/new/)
    path('reservations/new/', views.create_reservation, name='create_reservation'),

    # Страница личного кабинета со списком броней (адрес: /reservations/my/)
    path('reservations/my/', views.my_reservations, name='my_reservations'),
]
