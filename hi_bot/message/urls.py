from django.urls import path

from . import views

app_name = 'message'
urlpatterns = [
    # Главная страница сервиса. Доступна всем пользователям.
    path('', views.index, name='index'),
    # Страница статистики сервиса. Доступна модераторам и администраторам.
    path('dashboard/', views.dashboard, name='dashboard'),
    # Страница изменения ответа бота. Доступна модераторам и администраторам.
    path(
        'message/<int:message_id>/edit/',
        views.message_edit,
        name='message_edit'
    ),
]
