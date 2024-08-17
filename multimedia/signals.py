from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from subscription.models import UserLimits


@receiver(post_save, sender=User)
def create_user_limits(sender, instance, created, **kwargs):
    if created:  # Создаем только при создании нового пользователя
        UserLimits.objects.create(user=instance)

