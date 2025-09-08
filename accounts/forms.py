from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AdminUserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import CustomUser


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("ایمیل قبلاً ثبت شده است.")
        return email

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserForm(AdminUserCreationForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("ایمیل قبلاً ثبت شده است.")
        return email

    class Meta(AdminUserCreationForm.Meta):
        model = CustomUser


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser


class UserPasswordReset(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            raise ValidationError("ایمیل وجود ندارد.")
        return email
