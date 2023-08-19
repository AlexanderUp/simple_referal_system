from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.mixins import phone_number_pattern
from users.models import AuthorizationAttempt

User = get_user_model()


class AuthorizationCodeSerializer(serializers.Serializer):
    authorization_code = serializers.CharField(min_length=4, max_length=4)


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(phone_number_pattern)


class UserLoginSerializer(AuthorizationCodeSerializer):
    def validate_authorization_code(self, auth_code):
        if not AuthorizationAttempt.objects.filter(
            authorization_code=auth_code,
        ).exists():
            raise serializers.ValidationError('Incorrect authorization code.')
        return auth_code


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class SimpleUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            'phone_number',
        ]


class UserSerializer(BaseUserSerializer):
    invited_by = serializers.SlugRelatedField(slug_field='phone_number', read_only=True)
    invitees = serializers.SlugRelatedField(
        slug_field='phone_number',
        many=True,
        read_only=True,
    )

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'phone_number',
            'invite_code',
            'invited_by',
            'invitees',
        ]


class UserInviteSerializer(serializers.Serializer):
    invite_code = serializers.CharField(min_length=6, max_length=6)
