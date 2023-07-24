import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime as dt

import requests
from aiogram import Bot
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import django
from django.http import Http404
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from hi_bot.settings import TOKEN, API
from core import parsing_news
from message.models import User, Messages

BUTTONS = (
    KeyboardButton('/start'),
    KeyboardButton('/help'),
    KeyboardButton('/weather'),
    KeyboardButton('/news'),
)

PLEASE_REGISTER = (
    'Хей приятель, чтобы пользоваться мной зарегайся на нашем '
    'крутом сервисе. \nПри регистрации необходимо чтобы твой логин '
    'в телеге совпадал с логином на нашем сервисе:)'
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    filename='program.log',
    filemode='w',
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
handler = RotatingFileHandler('my_logger.log', maxBytes=5000000, backupCount=5)
logger.addHandler(handler)

bot = Bot(
    token=TOKEN
)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    try:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*BUTTONS)
        user = get_object_or_404(User, username=message.chat.username)
        answer = Messages.objects.create(
            recipient=user,
            command_response=Messages.Commands.START
        )
        await message.reply(
            f'Привет {answer.recipient}. {answer.command_response}',
            reply_markup=keyboard
        )
    except Http404:
        await message.reply(PLEASE_REGISTER)
    except Exception as error:
        await message.reply(
            f'Упс, произошла какая то ошибка -> вот она: {error}')
        logger.warning(error)


@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    try:
        user = get_object_or_404(User, username=message.chat.username)
        answer = Messages.objects.create(
            recipient=user,
            command_response=Messages.Commands.HELP
        )
        await message.reply(answer.command_response)
    except Http404:
        await message.reply(PLEASE_REGISTER)
    except Exception as error:
        await message.reply(
            f'Упс, произошла какая то ошибка -> вот она: {error}')
        logger.warning(error)


@dp.message_handler(commands=['news'])
async def get_news(message: Message):
    try:
        user = get_object_or_404(User, username=message.chat.username)
        date_timestamp, url, desc, title = parsing_news.main()
        answer = Messages.objects.create(
            recipient=user,
            description=desc,
            title=title,
            pub_date=dt.fromtimestamp(date_timestamp),
            link=url,
            command_response=Messages.Commands.NEWS
        )
        await message.reply(
            f'{answer.command_response} \n {answer.pub_date} \n {answer.link}'
        )
    except Http404:
        await message.reply(PLEASE_REGISTER)
    except Exception as error:
        await message.reply(
            f'Упс, произошла какая то ошибка -> вот она: {error}')
        logger.warning(error)


@dp.message_handler(commands=['weather'])
async def get_city(message: Message):
    try:
        await message.reply(
            'Напиши название города на англ в котором будем искать погоду'
        )
    except Exception as error:
        await message.reply(
            f'Упс, произошла какая то ошибка -> вот она: {error}')
        logger.warning(error)


@dp.message_handler()
async def get_weather(message: Message):
    try:
        user = get_object_or_404(User, username=message.chat.username)
        r = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?q=\n'
            f'{message.text.split()[-1]}&appid={API}&units=metric'
        )
        data = r.json()
        answer = Messages.objects.create(
            recipient=user,
            city=data.get('name'),
            temp=data.get('main').get('temp'),
            humidity=data.get('main').get('humidity'),
            sunrise=dt.fromtimestamp(data.get('sys').get('sunrise')),
            command_response=Messages.Commands.WEATHER
        )
        await message.reply(
            f'{answer.command_response} \n'
            f'В городе {answer.city} сейчас {answer.temp}°. \n'
            f'Влажность воздуха: {answer.humidity}. \n'
            f'Восход солнца: {answer.sunrise}. \n'
            f'\U00002620 Будь здоров:)'
        )
        logger.warning(answer)
    except Http404:
        await message.reply(PLEASE_REGISTER)
    except Exception as error:
        await message.reply(
            '\U00002620 Проверь название города, бро:)\n'
            'Мб ты пишешь на русском или с ошибками или вообще не указал?'
        )
        logger.warning(error)


class Command(BaseCommand):
    help = 'Включение телеграмм бота'

    def handle(self, *args, **kwargs):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        django.setup()
        executor.start_polling(dp)
