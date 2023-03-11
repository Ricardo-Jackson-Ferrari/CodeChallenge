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

from .models import User as _User
from .models import UserNotActivated as _UserNotActivated

__all__ = [
    'authenticate_user',
    'generete_url_for_active_account',
    'set_active_account',
    'active_account_send_mail',
    'UserNotActivated',
]
UserNotActivated = _UserNotActivated


def authenticate_user(email: str, password: str):
    user = _authenticate(username=email, password=password)
    if user:
        return user

    user_check = _User.objects.get(email=email)

    if user_check.check_password(password):
        raise UserNotActivated

    raise _User.DoesNotExist


def generete_url_for_active_account(user: _User) -> str:
    protocol = 'http' if _settings.DEBUG else 'https'
    domain = _settings.DOMAIN
    uid = _urlsafe_base64_encode(_force_bytes(user.pk))
    token = _default_token_generator.make_token(user)

    return f"{protocol}://{domain}{_reverse('account:active_account', kwargs={'uidb4': uid, 'token': token})}"


def set_active_account(uidb4: str, token: str) -> bool:
    uid = _force_str(_urlsafe_base64_decode(uidb4))
    try:
        user = _User.objects.get(pk=uid)

        if _default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return True
        else:
            return False
    except _User.DoesNotExist:
        return False


@_shared_task(bind=True, max_retries=5, default_retry_delay=2)
def active_account_send_mail(self, user_id):
    user = _User.objects.get(pk=user_id)
    active_url = generete_url_for_active_account(user)
    subject = 'Ative sua conta'
    mail_body = _render_to_string(
        'account/mails/active_account.html', {'active_url': active_url}
    )
    email = _EmailMessage(subject, mail_body, to=[user.email])

    if email.send():
        return mail_body

    self.retry(countdown=2**self.request.retries)
    raise Exception('Erro')
