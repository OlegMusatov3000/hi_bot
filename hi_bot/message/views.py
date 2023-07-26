from django.shortcuts import (
    render,
    get_object_or_404,
    get_list_or_404,
    redirect
)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Answer, User
from .forms import MessageForm


def paginate(request, object, count=10):
    return Paginator(object, count).get_page(request.GET.get('page'))


def index(
    request,
    title='Вcе ответы бота',
    template='message/index.html'
):
    messages = Answer.objects.order_by('-created').all()
    context = {
        'page_obj': paginate(request, messages),
        'title': title,
    }
    return render(request, template, context)


@login_required
def dashboard(request, template='message/dashboard.html'):
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
    if request.user.role in (User.UsersRole.ADMIN, User.UsersRole.MODERATOR):
        message = get_object_or_404(Answer, id=message_id)
        if request.method == 'POST':
            form = MessageForm(
                request.POST,
                files=request.FILES or None,
                instance=message
            )
            if form.is_valid:
                message = form.save(commit=False)
                message.save()
                return (redirect('message:index'))
        form = MessageForm(
            files=request.FILES or None,
            instance=message
        )
        context = {
            'form': form,
            'title': title,
        }
        return render(request, template, context)
    return (redirect('message:index'))
