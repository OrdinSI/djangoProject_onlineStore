from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, UserLoginView, UserConfirmEmailView, EmailConfirmedView, \
    EmailFailedView, EmailConfirmationSentView, UserPasswordResetView, UserPasswordResetConfirmView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('confirm_email/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('email_failed/', EmailFailedView.as_view(), name='email_failed'),
    path('email_confirmation_sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('set_new_password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm')
]
