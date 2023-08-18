from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import AuthorizationAttempt

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'phone_number',
        'invite_code',
        'invited_by',
    )


class AuthorizationAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'phone_number',
        'is_authorized',
        'created',
    )


admin.site.register(User, UserAdmin)
admin.site.register(AuthorizationAttempt, AuthorizationAttemptAdmin)
