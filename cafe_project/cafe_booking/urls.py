from django.contrib import admin
from django.urls import path, include  # Импортируем функцию include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Стандартная админка Django
    path('admin/', admin.site.merge_with_urls if hasattr(admin.site, 'merge_with_urls') else admin.site.urls),

    # Подключаем все маршруты из нашего приложения bookings
    path('', include('bookings.urls')),

    # Встроенные маршруты Django для авторизации (вход и выход)
    path('login/', auth_views.LoginView.as_view(template_name='bookings/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Эта строчка критически важна: она разрешает Django показывать загруженные картинки столиков в браузере
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

