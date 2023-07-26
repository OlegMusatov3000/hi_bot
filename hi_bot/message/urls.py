from django.urls import path

from . import views

app_name = 'message'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'message/<int:message_id>/edit/',
        views.message_edit,
        name='message_edit'
    ),
]
