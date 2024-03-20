from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm, UserAuthenticationForm
from users.models import User


class UserAuthenticationMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Вы уже авторизованы. Вы не можете посетить эту страницу.')
            raise PermissionDenied
        return True

    def handle_no_permission(self):
        return redirect(reverse('users:login'))


class RegisterView(UserAuthenticationMixin, CreateView):
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

        print("Перед генерацией токена:")
        print(user)
        print(user.password)
        print(user.last_login)
        print(user.email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        uid_id = urlsafe_base64_decode(uid)
        user_id = User.objects.get(pk=uid_id)
        print(f"хЭШ В БАЗЕ  {user_id.password}")


        activation_url = reverse('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        print(f'{settings.BASE_URL}{activation_url}')

        # send_mail(
        #     subject='Подтвердите свой электронный адрес.',
        #     message=f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: '
        #             f'{settings.BASE_URL}{activation_url}',
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[self.object.email],
        #     fail_silently=False,
        # )
        return super().form_valid(form)


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        print("Перед проверкой токена:")
        print(token)
        print(user)
        print(user.password)
        print(user.last_login)
        print(user.email)
        print(default_token_generator.check_token(user, token))

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_failed')


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
