from django.urls import path

from api.views import AuthorizationAttemptView, InviteView, LoginView, UserView

app_name = 'api'

urlpatterns = [
    path('v1/authorize/', AuthorizationAttemptView.as_view(), name='authorize'),
    path('v1/login/', LoginView.as_view(), name='login'),
    path('v1/users/me/', UserView.as_view(), name='users-me'),
    path('v1/users/invite/', InviteView.as_view(), name='users-invite'),
]
