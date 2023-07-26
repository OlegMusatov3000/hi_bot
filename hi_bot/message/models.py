from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import COMMANDS


class User(AbstractUser):
    """Класс пользователей."""
    class UsersRole(models.TextChoices):
        ANON = 'anonymous', _('анон')
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Админ')

    role = models.CharField(
        'Пользовательская роль',
        max_length=30,
        blank=True,
        choices=UsersRole.choices,
        default=UsersRole.USER
    )

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)


class Answer(models.Model):
    class Command(models.TextChoices):
        START = COMMANDS['start'], _('START')
        HELP = COMMANDS['help'], _('HELP')
        NEWS = COMMANDS['news'], _('NEWS')
        WEATHER = COMMANDS['weather'], _('WEATHER')

    recipient = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='recipient',
        verbose_name='Получатель сообщения'
    )

    created = models.DateTimeField(
        'Время получения',
        auto_now=True
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    title = models.TextField(
        'Заголовок',
        blank=True,
        null=True
        )
    pub_date = models.DateTimeField(
        'Время получения',
        blank=True,
        null=True
    )
    command_response = models.TextField(
        'Команда для бота',
        choices=Command.choices)
    link = models.URLField(
        'Ссылка на новость',
        blank=True,
        null=True
    )
    image = models.ImageField(
        'Картинка',
        upload_to=settings.MEDIA_FOR_MESSAGE,
        blank=True,
        null=True
    )
    sunrise = models.DateTimeField(
        'Восход солнца',
        blank=True,
        null=True
    )
    humidity = models.FloatField(
        'Влажность воздуха',
        blank=True,
        null=True,
    )
    city = models.CharField(
        'Влажность воздуха',
        max_length=30,
        blank=True,
        null=True,
    )
    temp = models.FloatField(
        'Температура воздуха в С°',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.command_response}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ('-created',)
