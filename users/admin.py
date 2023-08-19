from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import AuthorizationAttempt

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'phone_number',
        'invite_code',
        'invited_by',
    )
    ordering = ('-pk',)
    empty_value_display = 'no_value'
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            ('Personal Info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'phone_number',
                    'invite_code',
                    'invited_by',
                ),
            },
        ),
        (
            ('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            ('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'password1',
                    'password2',
                    'phone_number',
                ),
            },
        ),
    )


class AuthorizationAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'phone_number',
        'authorization_code',
    )
    readonly_fields = ('authorization_code',)


admin.site.register(User, UserAdmin)
admin.site.register(AuthorizationAttempt, AuthorizationAttemptAdmin)
