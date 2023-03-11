from celery import shared_task as _shared_task
from django.conf import settings as _settings
from django.contrib.auth import authenticate as _authenticate
from django.contrib.auth.tokens import (
    default_token_generator as _default_token_generator,
)
from django.core.mail import EmailMessage as _EmailMessage
from django.template.loader import render_to_string as _render_to_string
from django.urls import reverse as _reverse
from django.utils.encoding import force_bytes as _force_bytes
from django.utils.encoding import force_str as _force_str
from django.utils.http import urlsafe_base64_decode as _urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode as _urlsafe_base64_encode
from .models import SimpleUser
__all__ = [
    'create_account_send_mail',
]

@_shared_task(bind=True, max_retries=5, default_retry_delay=2)
def create_account_send_mail(self, user_id, user_email):
    active_url = 'url'
    subject = 'Ative sua conta'
    mail_body = _render_to_string(
        'account/mails/active_account.html', {'active_url': active_url}
    )
    email = _EmailMessage(subject, mail_body, to=[user_email])

    if email.send():
        SimpleUser.objects.get(pk=user_id).url = active_url
        return mail_body
