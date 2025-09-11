"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from accounts.views import SignUp, PasswordReset, LoginPageView, PasswordChange, SentEmailReset, PasswordResetConfirm, \
    PasswordResetComplete, Dashboard, Logout

app_name = 'accounts'

urlpatterns = [
    path("signup/", SignUp.as_view(), name='signup'),
    path("login/", LoginPageView.as_view(), name='login'),
    path("logout/", Logout.as_view(), name='logut'),
    path("password_reset/", PasswordReset.as_view(), name='password_reset'),
    path("password_change/", PasswordChange.as_view(), name='password_change'),
    path("password_reset_sent/", SentEmailReset.as_view(), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path("reset/done/", PasswordResetComplete.as_view(), name="password_reset_complete"),
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
]
