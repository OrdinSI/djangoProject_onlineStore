from datetime import timedelta, datetime

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView,  PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from jose import jwt, JWTError

from users.forms import UserRegisterForm, UserProfileForm, UserAuthenticationForm, UserPasswordResetForm, \
    UserSetNewPasswordForm
from users.models import User


class RegisterView(CreateView):
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
        user.is_active = True
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
    template_name = 'users/email_confirmed.html'


class EmailFailedView(TemplateView):
    template_name = 'users/email_failed.html'


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserLoginView(LoginView):
    model = User
    form_class = UserAuthenticationForm
    template_name = 'users/login.html'


class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    model = User
    form_class = UserPasswordResetForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('catalog:product_list')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_email.html'


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    model = User
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('catalog:product_list')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

