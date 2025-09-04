from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, LoginView, PasswordChangeView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import UserCreateForm, UserPasswordReset


class SignUp(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('accounts:login')


class PasswordReset(PasswordResetView):
    template_name = 'registration/password_reset.html'
    form_class = UserPasswordReset
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'registration/password_change.html'


class LoginPageView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class SentEmailReset(PasswordResetDoneView):
    template_name = 'registration/sent_reset_password.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
