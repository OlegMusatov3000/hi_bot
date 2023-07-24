from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Messages
from .forms import MessageForm

NUMBER_OF_POSTS = 10


def paginate(request, messages):
    paginator = Paginator(messages, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    user_is_staff = False
    if (
        request.user.is_authenticated
        and request.user.role in ('moderator', 'admin')
    ):
        user_is_staff = True
    messages = Messages.objects.order_by('-created').all()
    title = 'Вcе ответы бота'
    context = {
        'page_obj': paginate(request, messages),
        'title': title,
        'user_is_staff': user_is_staff
    }
    template = 'message/index.html'
    return render(request, template, context)


@login_required
def bot_change(request, post_id):
    pass


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
