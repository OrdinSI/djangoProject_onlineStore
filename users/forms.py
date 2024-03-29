from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """User registration form."""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """User profile"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'country', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserAuthenticationForm(StyleFormMixin, AuthenticationForm):
    """User authentication"""
    pass


class UserPasswordResetForm(StyleFormMixin, PasswordResetForm):
    """User password reset form"""
    class Meta:
        model = User
        fields = ('email',)

# class UserSetNewPasswordForm(StyleFormMixin, SetPasswordForm):
#     class Meta:
#         model = User
#         fields = ('new_password1', 'new_password2')
