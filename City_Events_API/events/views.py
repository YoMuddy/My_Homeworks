from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.models import User

# Подключаем наши классы-переводчики из соседнего файла serializers.py
from .serializers import RegisterSerializer, UserReadOnlySerializer


class UserListCreateAPIView(APIView):

    # Специальный метод Django, который гибко распределяет права доступа для страницы
    def get_permissions(self):
        # Если клиент делает POST-запрос (отправляет данные формы регистрации)
        if self.request.method == 'POST':
            # Разрешаем доступ абсолютно всем анонимным пользователям
            return [AllowAny()]

        # Если клиент делает GET-запрос (пытается просто посмотреть список)
        # Блокируем доступ для всех, кроме пользователей со статусом "Администратор"
        return [IsAdminUser()]

    # Логика, которая срабатывает при попытке регистрации (POST)
    def post(self, request):
        # Берем присланные пользователем данные из request.data и передаем в валидатор
        serializer = RegisterSerializer(data=request.data)

        # Запускаем автоматическую проверку (заполнены ли поля, уникально ли имя)
        if serializer.is_valid():
            # Если всё отлично, вызываем сохранение в базу данных
            serializer.save()
            # Возвращаем клиенту текст с его созданным аккаунтом и статус 201 (Создано)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Если данные с ошибками, возвращаем список этих ошибок и статус 400 (Плохой запрос)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Логика, которая срабатывает при попытке просмотра списка (GET)
    def get(self, request):
        # Делаем запрос к базе данных и вытаскиваем абсолютно все существующие аккаунты
        all_users = User.objects.all()

        # Передаем этот массив аккаунтов в наш сериализатор для вывода на экран.
        # Параметр many=True обязателен, чтобы робот понял, что перед ним список, а не один юзер
        serializer = UserReadOnlySerializer(all_users, many=True)

        # Возвращаем готовый отформатированный список обратно клиенту со статусом 200 OK
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.utils import timezone
from .models import Event
from .serializers import EventSerializer


# Эндпоинт для просмотра списка будущих мероприятий
class ActiveEventListAPIView(APIView):
    # Доступ к списку событий разрешаем абсолютно всем гостям
    permission_classes = [AllowAny]

    def get(self, request):
        # Получаем текущее время на компьютере/сервере
        now = timezone.now()

        # Фильтруем таблицу: выбираем только те события, где время проведения больше (гт), чем сейчас
        actual_events = Event.objects.filter(meeting_time__gt=now)

        # Передаем этот список в сериализатор вывода
        serializer = EventSerializer(actual_events, many=True)

        # Отдаем JSON-список клиенту
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.permissions import IsAuthenticated


# 1. ЭНДПОИНТ ДЛЯ ПОДПИСКИ НА СОБЫТИЕ
class SubscribeToEventAPIView(APIView):
    # Доступ разрешен только авторизованным пользователям (кто вошел по токену)
    permission_classes = [IsAuthenticated]

    # Используем метод POST для совершения действия подписки
    def post(self, request, event_id):
        try:
            # Ищем событие по его ID в базе данных
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            # Если события с таким номером нет, возвращаем ошибку 404
            return Response({"error": "Мероприятие не найдено"}, status=status.HTTP_404_NOT_FOUND)

        # Добавляем текущего пользователя (request.user) в список участников этого события
        event.users.add(request.user)

        return Response({"message": f"Вы успешно записались на мероприятие: {event.name}"}, status=status.HTTP_200_OK)


# 2. ЭНДПОИНТ ДЛЯ ПРОСМОТРА ЛИЧНЫХ ПОДПИСОК
class MyEventsAPIView(APIView):
    # Пускаем только авторизованных пользователей
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Достаем из базы только те события, на которые подписан текущий пользователь
        # Свойство .events появилось благодаря related_name='events' в нашей модели!
        my_events = request.user.events.all()

        # Передаем список в наш готовый сериализатор событий
        serializer = EventSerializer(my_events, many=True)

        # Отдаем список пользователю
        return Response(serializer.data, status=status.HTTP_200_OK)
