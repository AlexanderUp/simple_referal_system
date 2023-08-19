import functools

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from users.mixins import PhoneNumberMixin
from users.utils import get_random_str

authorization_code_generator = functools.partial(get_random_str, 2)
invite_code_generator = functools.partial(get_random_str, 3)


class User(PhoneNumberMixin, AbstractUser):
    invite_code = models.CharField(
        max_length=6,
        default=invite_code_generator,
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

    def save(self, *args, **kwargs):
        if self.invited_by and self.invited_by.phone_number == self.phone_number:
            raise ValidationError('Self invitation prohibited.')
        super().save(*args, **kwargs)


class AuthorizationAttempt(PhoneNumberMixin):
    authorization_code = models.CharField(
        max_length=4,
        default=authorization_code_generator,
        unique=True,
        verbose_name='Authorization code',
        help_text='Authorization code',
    )

    class Meta:
        verbose_name = 'Authorization attempt'
        verbose_name_plural = 'Authorization attempts'
        ordering = ('-pk',)

    def __str__(self):
        return f'Authorization attempt ({self.phone_number})'
