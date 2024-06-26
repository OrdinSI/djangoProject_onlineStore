import random
import string
from datetime import timedelta, datetime

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, TemplateView, FormView, View
from jose import jwt, JWTError

from users.forms import UserRegisterForm, UserProfileForm, UserAuthenticationForm, UserPasswordResetForm
from users.models import User


class RegisterView(CreateView):
    """Register view"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:email_confirmation_sent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        payload = {
            'sub': uid,
            'exp': datetime.utcnow() + timedelta(seconds=86400)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        activation_url = reverse('users:confirm_email', kwargs={'token': token})

        send_mail(
            subject='Подтвердите свой электронный адрес.',
            message=f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты:'
                    f'{settings.BASE_URL}{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class UserConfirmEmailView(View):
    """User confirm email view."""

    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            uid_data = payload.get('sub')
            uid = urlsafe_base64_decode(uid_data)
            user = User.objects.get(pk=uid)
            if payload.get('exp') < datetime.utcnow().timestamp():
                return redirect('users:email_failed')
        except(jwt.ExpiredSignatureError, JWTError, User.DoesNotExist):
            return redirect('users:email_failed')

        user.is_active = True
        user.save()
        login(request, user)
        return redirect('users:email_confirmed')


class EmailConfirmedView(TemplateView):
    """Email confirmed view."""
    template_name = 'users/email_confirmed.html'


class EmailFailedView(TemplateView):
    """Email not confirmed"""
    template_name = 'users/email_failed.html'


class EmailConfirmationSentView(TemplateView):
    """Email confirmation"""
    template_name = 'users/email_confirmation_sent.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    """Profile view."""
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserLoginView(LoginView):
    """User login view."""
    model = User
    form_class = UserAuthenticationForm
    template_name = 'users/login.html'


# class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
#     model = User
#     form_class = UserPasswordResetForm
#     template_name = 'users/user_password_reset.html'
#     success_url = reverse_lazy('catalog:product_list')
#     success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
#     subject_template_name = 'users/email/password_subject_reset_mail.txt'
#     email_template_name = 'users/email/password_reset_email.html'
#
#
# class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
#     model = User
#     form_class = UserSetNewPasswordForm
#     template_name = 'users/user_password_set_new.html'
#     success_url = reverse_lazy('users:login')
#     success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'


class UserPasswordResetView(FormView):
    """User password reset view."""
    template_name = 'users/user_password_reset.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('users:user_password_sent')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()

        if user is not None:
            characters = string.ascii_letters + string.digits
            new_password = ''.join(random.choice(characters) for i in range(12))

            user.password = make_password(new_password)
            user.save()

            subject = 'Восстановление пароля'
            message = f'Ваш новый пароль: {new_password}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return super().form_valid(form)


class UserPasswordSentView(TemplateView):
    """User password sent view."""
    template_name = 'users/user_password_sent.html'
