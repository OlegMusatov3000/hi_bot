from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
)
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # Страница выхода.
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    # Страница регистрации пользователей.
    path('signup/', views.SignUp.as_view(), name='signup'),
    # Страница авторизации пользователей.
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    # Страница смена паролей пользователей.
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='users/password_change_form.html'),
        name='password_change'),
    # Страница успешного изменения пароля пользователя.
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'),
        name='password_change_done'),
]
