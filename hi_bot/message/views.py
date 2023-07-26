from django.shortcuts import (
    render,
    get_object_or_404,
    get_list_or_404,
    redirect
)
from django.contrib.auth.decorators import login_required

from core.utils import paginate
from .models import Answer, User
from .forms import AnswerForm


def index(
    request,
    title='Вcе ответы бота',
    template='message/index.html'
):
    '''
    Обработчик для главной страницы.
    Отправляет в шаблон пагинатор со всеми объектами модели "Answer".
    Шаблон показывает все сообщения бота.
    '''
    messages = Answer.objects.all()
    context = {
        'page_obj': paginate(request, messages),
        'title': title,
    }
    return render(request, template, context)


@login_required
def dashboard(request, template='message/dashboard.html'):
    '''
    Обработчик для страницы статистики сервиса.
    Отправляет в шаблон пагинатор со всеми объектами модели "User".
    При отсутствии запросов выдаст 404 и покажет пользователю кастомный шаблон.
    Показывает статистику сервиса о количествах запросов
    и самых популярных командах каждого пользователя.
    '''
    if request.user.role in ('moderator', 'admin'):
        messages_list = get_list_or_404(Answer)
        users_list = get_list_or_404(User)
        context = {
            'messages_list': messages_list,
            'messages_count': len(messages_list),
            'users_count': len(users_list),
            'page_obj': paginate(request, users_list),
        }
        return render(request, template, context)
    return (redirect('message:index'))


@login_required
def message_edit(
    request,
    message_id,
    template='message/edit_message.html',
    title='Меняем сообщение бота',
):
    '''
    Обработчик для страницы редактирования сообщения.
    Отправляет в шаблон форму редактирования объекта модели "Answer".
    Дает возможность администраторам и модераторам редактировать ответы бота.
    '''
    if request.user.role in (User.UsersRole.ADMIN, User.UsersRole.MODERATOR):
        message = get_object_or_404(Answer, id=message_id)
        if request.method == 'POST':
            form = AnswerForm(
                request.POST,
                files=request.FILES or None,
                instance=message
            )
            if form.is_valid:
                message = form.save(commit=False)
                message.save()
                return (redirect('message:index'))
        form = AnswerForm(
            files=request.FILES or None,
            instance=message
        )
        context = {
            'form': form,
            'title': title,
        }
        return render(request, template, context)
    return (redirect('message:index'))
