from rest_framework import serializers
from django.contrib.auth.models import User

# Класс для проверки данных при создании нового аккаунта
class RegisterSerializer(serializers.ModelSerializer):
    # Указываем, что пароль можно только отправить. В ответах сервера он отображаться не будет
    password = serializers.CharField(write_only=True)

    class Meta:
        # Связываем этот сериализатор со встроенной таблицей пользователей Django
        model = User
        # Четко перечисляем поля, которые должен прислать клиент для создания аккаунта
        fields = ['username', 'email', 'password']

    # Метод, который берет проверенные данные и физически создает запись в базе
    def create(self, validated_data):
        # Метод create_user автоматически шифрует пароль перед сохранением в базу
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Новый класс для безопасного вывода списка пользователей на экран
class UserReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        # Работаем с той же таблицей пользователей
        model = User
        # Показываем только общую информацию. Пароль сюда включать категорически нельзя
        fields = ['id', 'username', 'email']

# Добавляем импорт нашей модели событий в самый верх файла или используем текущий
from .models import Event

# Класс для красивого вывода событий на экран
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        # Указываем, какие поля таблицы мы хотим отдавать пользователям
        fields = ['id', 'name', 'meeting_time', 'description']
