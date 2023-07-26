from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    '''
    Обработчик для страницы регистрации.
    Реализует функционал регистрации.
    Бот будет отвечать на команду пользователя при условии совпадения
    логинов из Телеграма и сервиса Hi_bot.
    '''

    form_class = CreationForm
    success_url = reverse_lazy('message:index')
    template_name = 'users/signup.html'
