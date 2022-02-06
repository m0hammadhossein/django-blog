from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import \
    (LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView,
     PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from accounts.mixins import FieldsMixin, FormValidMixin, AuthorAccessMixin, SuperUserAccessMixin, AuthorsAccessMixin
from blog.models import Article
from .forms import ProfileForm, SignupForm
from django.contrib.auth import get_user_model
from .token import account_activation_token

User = get_user_model()


class ArticleList(AuthorsAccessMixin, ListView):
    context_object_name = 'articles'
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        return Article.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixin, FieldsMixin, FormValidMixin, CreateView):
    model = Article
    template_name = 'registration/article-create-update.html'


class ArticleUpdate(AuthorAccessMixin, FieldsMixin, FormValidMixin, UpdateView):
    model = Article
    template_name = 'registration/article-create-update.html'


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('accounts:home')
    template_name = 'registration/delete.html'


class Profile(LoginRequiredMixin, UpdateView):
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LoginAccount(LoginView):

    def get_success_url(self):
        redirect_url = super().get_redirect_url()
        if redirect_url:
            return redirect_url
        elif self.request.user.is_superuser or self.request.user.is_author:
            return reverse_lazy('accounts:home')
        return reverse_lazy('accounts:profile')


class PasswordChange(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'registration/password_changed.html'


class PasswordReset(PasswordResetView):
    email_template_name = 'registration/password_reset_email_text.html'
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/password_reseted.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'registration/password_reset_completed.html'


class LogoutAccount(LogoutView):
    next_page = reverse_lazy('accounts:login')


def activate(request, uidb64, token):
    context = {'activate': False}
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        context['activate'] = True
    return render(request, 'registration/email_activate.html', context=context)


class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('registration/email_template.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        send_mail(mail_subject, message, 'youremail', [to_email])
        return render(self.request, 'registration/email_activate_url.html')
