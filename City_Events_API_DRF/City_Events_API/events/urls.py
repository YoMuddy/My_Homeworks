from django.urls import path
from .views import (
    UserListCreateAPIView,
    ActiveEventListAPIView,
    SubscribeToEventAPIView,
    MyEventsAPIView
)

urlpatterns = [
    # 1. Регистрация и просмотр пользователей администраторами
    path('users', UserListCreateAPIView.as_view(), name='user-list-create'),

    # 2. Просмотр списка всех актуальных мероприятий в городе
    path('events', ActiveEventListAPIView.as_view(), name='events-active'),

    # 3. Подписка на конкретное событие (передаем его ID в адресе, например: api/event/1)
    path('event/<int:event_id>', SubscribeToEventAPIView.as_view(), name='event-subscribe'),

    # 4. Просмотр только тех мероприятий, на которые записался текущий пользователь
    path('events/my', MyEventsAPIView.as_view(), name='events-my'),
]
