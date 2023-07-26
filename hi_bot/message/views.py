from django.shortcuts import (
    render,
    get_object_or_404,
    get_list_or_404,
    redirect
)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Messages, User
from .forms import MessageForm

NUMBER_OF_POSTS = 10


def paginate(request, messages):
    paginator = Paginator(messages, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    messages = Messages.objects.order_by('-created').all()
    title = 'Вcе ответы бота'
    context = {
        'page_obj': paginate(request, messages),
        'title': title,
    }
    template = 'message/index.html'
    return render(request, template, context)


@login_required
def dashboard(request):
    if request.user.role in ('moderator', 'admin'):
        messages_list = get_list_or_404(Messages)
        users_list = get_list_or_404(User)
        template = 'message/dashboard.html'
        context = {
            'messages_list': messages_list,
            'messages_count': len(messages_list),
            'users_count': len(users_list),
            'page_obj': paginate(request, users_list),
        }
        return render(request, template, context)
    return (redirect('message:index'))


@login_required
def message_edit(request, message_id):
    if request.user.role in ('moderator', 'admin'):
        message = get_object_or_404(Messages, id=message_id)
        template = 'message/edit_message.html'
        title = 'Меняем сообщение бота'

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
