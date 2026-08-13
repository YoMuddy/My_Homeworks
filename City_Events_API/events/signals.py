from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, User
from .tasks import send_email_task


@receiver(post_save, sender=Event)
def notify_users_about_new_event(sender, instance, created, **kwargs):
    """
    Сигнал уровня модели для автоматического оповещения пользователей
    в момент публикации нового контента.
    """
    # Логика срабатывает исключительно при создании новой записи (метод INSERT)
    if created:
        # Выборка пользователей, которые явно дали согласие на получение писем
        subscribers_emails = User.objects.filter(notify=True).values_list('email', flat=True)

        if subscribers_emails:
            subject = f"Новое мероприятие: «{instance.name}»!"
            msg = (
                f"Новое мероприятие: «{instance.name}»!\n\n"
                f"«{instance.description}».\n\n"
                f"Мероприятие проходит завтра в {instance.meeting_time.strftime('%H:%M')}."
            )
            # Постановка задачи рассылки в очередь брокера сообщений
            send_email_task.delay(subject, msg, list(subscribers_emails))
