from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (
    AuthorizationCodeSerializer,
    PhoneNumberSerializer,
    ResponseDocumentationAuthTokenSerializer,
    UserInviteSerializer,
    UserLoginSerializer,
    UserSerializer,
)
from api.task_related_utils import delay
from users.models import AuthorizationAttempt, authorization_code_generator

User = get_user_model()


class AuthorizationAttemptView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=PhoneNumberSerializer,
        responses={
            201: openapi.Response(
                'Phone number accepted',
                AuthorizationCodeSerializer,
            ),
            400: openapi.Response(
                'Bad request',
                PhoneNumberSerializer,
            ),
        },
    )
    @delay(2)
    def post(self, request, *args, **kwargs):
        phone_number_serializer = PhoneNumberSerializer(data=request.data)
        phone_number_serializer.is_valid(raise_exception=True)
        phone_number = phone_number_serializer.validated_data['phone_number']
        attempt, is_created = AuthorizationAttempt.objects.get_or_create(
            phone_number=phone_number,
        )
        if not is_created:
            attempt.authorization_code = authorization_code_generator()
            attempt.save()
        authorization_code_serializer = AuthorizationCodeSerializer(attempt)
        return Response(authorization_code_serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            201: openapi.Response(
                'Created',
                ResponseDocumentationAuthTokenSerializer,
            ),
            400: UserLoginSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authorization_code = serializer.validated_data['authorization_code']
        attempt = AuthorizationAttempt.objects.get(authorization_code=authorization_code)

        with transaction.atomic():
            user, is_created = User.objects.get_or_create(
                username=attempt.phone_number,
                phone_number=attempt.phone_number,
            )
            if is_created:
                user.set_unusable_password()
                user.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)


class UserView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('OK.', UserSerializer),
            401: 'Unauthorized.',
        },
    )
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InviteView(APIView):
    @swagger_auto_schema(
        request_body=UserInviteSerializer,
        responses={
            201: openapi.Response(
                'Created',
                UserSerializer,
            ),
            400: 'Bad request',
            401: 'Unauthorized.',
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = UserInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_invited_code = serializer.validated_data['invite_code']

        if request.user.invited_by:
            return Response(
                {
                    'Non-field errors': ['You already use invitation code earlier.'],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.user.invite_code == user_invited_code:
            return Response(
                {
                    'Non-field errors': ['Self invitation prohibited.'],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_invited_by = get_object_or_404(User, invite_code=user_invited_code)

        request.user.invited_by = user_invited_by
        request.user.save()
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
