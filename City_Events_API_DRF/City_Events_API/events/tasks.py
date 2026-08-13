from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Event, User


@shared_task
def send_email_task(subject, message, recipient_list):
    """
    Низкоуровневая изолированная задача Celery для асинхронной отправки почты.
    Вынесена в отдельный поток выполнения для снижения нагрузки на основной процесс API.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@cityevents.com',
        recipient_list=recipient_list,
        fail_silently=False,
    )


@shared_task
def check_reminders_periodic_task():
    """
    Периодическая фоновая задача (вызывается планировщиком Celery Beat).
    Сканирует базу данных на предмет приближающихся событий и инициирует рассылку.
    """
    now = timezone.now()

    # === Проверка мероприятий, стартующих через 24 часа ===
    one_day_later = now + timedelta(days=1)

    # Выбираем актуальные события в интервале суток, где напоминание еще не отправлялось
    events_1_day = Event.objects.filter(
        meeting_time__lte=one_day_later,
        meeting_time__gt=now,
        reminded_1_day=False
    )

    for event in events_1_day:
        # Получаем список адресов всех пользователей, зарегистрированных на событие
        emails = event.users.values_list('email', flat=True)

        if emails:
            subject = f"Напоминание о мероприятии: {event.name}"
            msg = (
                f"Уведомляем вас, что вы согласились посетить «{event.name}».\n\n"
                f"«{event.description}».\n\n"
                f"Мероприятие проходит завтра в {event.meeting_time.strftime('%H:%M')}."
            )
            # Передача отправки писем в асинхронный воркер
            send_email_task.delay(subject, msg, list(emails))

        # Фиксация отправки уведомления в базе данных
        event.reminded_1_day = True
        event.save()

    # === Проверка мероприятий, стартующих через 6 часов ===
    six_hours_later = now + timedelta(hours=6)

    events_6_hours = Event.objects.filter(
        meeting_time__lte=six_hours_later,
        meeting_time__gt=now,
        reminded_6_hours=False
    )

    for event in events_6_hours:
        emails = event.users.values_list('email', flat=True)
        if emails:
            subject = f"Срочное напоминание: до {event.name} осталось 6 часов!"
            msg = f"Напоминаем, что мероприятие «{event.name}» начнется совсем скоро — через 6 часов!"
            send_email_task.delay(subject, msg, list(emails))

        # Фиксация отправки срочного уведомления
        event.reminded_6_hours = True
        event.save()
