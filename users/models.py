import functools

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from users.mixins import PhoneNumberMixin
from users.utils import get_random_str

random_str_4 = functools.partial(get_random_str, 2)
random_str_6 = functools.partial(get_random_str, 3)


class User(PhoneNumberMixin, AbstractUser):
    invite_code = models.CharField(
        max_length=6,
        default=random_str_6,
        unique=True,
        verbose_name='Invite code',
        help_text='Invite code',
    )
    invited_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='invitees',
        null=True,
        blank=True,
        verbose_name='Invited by',
        help_text='Invited by',
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-pk',)

    def __str__(self):
        return f'User <{self.username}> ({self.phone_number})'


class AuthorizationAttempt(PhoneNumberMixin):
    authorization_code = models.CharField(
        max_length=4,
        default=random_str_4,
        unique=True,
        verbose_name='Authorization code',
        help_text='Authorization code',
    )
    is_authorized = models.BooleanField(
        default=False,
        verbose_name='Is authorized',
        help_text='Is authorized?',
    )
    created = models.DateTimeField(
        default=timezone.now,
        verbose_name='Created',
        help_text='Authorization attempt created at',
    )

    class Meta:
        verbose_name = 'Authorization attempt'
        verbose_name_plural = 'Authorization attempts'
        ordering = ('-pk',)

    def __str__(self):
        return f'Authorization attempt ({self.phone_number})'
