from django.core.validators import RegexValidator
from django.db import models

phone_number_pattern = '^\\+7[0-9]{10}$'
phone_number_reg_validator = RegexValidator(phone_number_pattern)


class PhoneNumberMixin(models.Model):
    phone_number = models.CharField(
        max_length=12,
        validators=(phone_number_reg_validator,),
        unique=True,
        verbose_name='Phone number',
        help_text='Phone number',
    )

    class Meta:
        abstract = True
