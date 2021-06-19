# Create your models here.
from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from user.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True)

    image = models.ImageField(upload_to='user/images', null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: List[str] = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return f'{self.email}'

    @cached_property
    def token(self):
        return str(AccessToken.for_user(self))


@receiver(post_save, sender=User)
def refresh_token(instance: User, **___):
    RefreshToken.for_user(instance)
