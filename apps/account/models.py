from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, max_length=255)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email




class SimpleUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)


class Profile(models.Model):
    user = models.OneToOneField(SimpleUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> None:
        return self.user
    





