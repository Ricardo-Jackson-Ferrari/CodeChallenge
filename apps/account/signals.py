from .models import SimpleUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from .facade import create_account_send_mail


@receiver(post_save, sender=SimpleUser)
def active_account_mail(sender, instance, created, **kwargs):
    if created:
        create_account_send_mail.delay(user_id=instance.id, user_email=instance.email)
