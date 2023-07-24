from django.urls import path

from . import views

app_name = 'message'
urlpatterns = [
    path('', views.index, name='index'),
    path('change/', views.bot_change, name='bot_change'),
    path(
        'message/<int:message_id>/edit/',
        views.message_edit,
        name='message_edit'),
]
