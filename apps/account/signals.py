from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .facade import active_account_send_mail


@receiver(post_save, sender=get_user_model())
def active_account_mail(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        active_account_send_mail.delay(user_id=instance.id)
