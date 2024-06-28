
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notification, Like, Comment


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            message=f'Добро пожаловать! Вы можете дополнить свои данные в настройках профиля.'
        )


@receiver(post_save, sender=Like)
def post_liked(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.post.author,
            message=f'Пользователь {instance.user.username} лайкнул ваш пост.'
        )

@receiver(post_save, sender=Comment)
def post_commented(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.post.author,
            message=f'Пользователь {instance.user.username} прокомментировал ваш пост.'
        )
