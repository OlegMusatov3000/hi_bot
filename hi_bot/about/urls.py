from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    # Страница автора проекта.
    path('author/', views.AboutAuthorView.as_view(), name='author'),
    # Страница использованных в проекте технологий.
    path('tech/', views.AboutTechView.as_view(), name='tech'),
]
