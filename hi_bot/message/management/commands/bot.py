import os
import sys
import logging
import datetime
from datetime import datetime as dt

import django
from aiogram import Bot
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from django.utils import timezone
from django.http import Http404
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from hi_bot.settings import TOKEN
from core.utils import parsing_news, get_weather
from message.models import User, Answer

PLEASE_REGISTER = (
    'Хей приятель, чтобы пользоваться мной зарегайся на нашем '
    'крутом сервисе. \nПри регистрации необходимо чтобы твой логин '
    'в телеге совпадал с логином на нашем сервисе:)'
)
UNKNOWN_ERROR = 'Упс, произошла какая то ошибка -> вот она: '

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=(
        logging.StreamHandler(sys.stdout),
    )
)

logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(
    message: Message,
    buttons=(
        KeyboardButton('/start'),
        KeyboardButton('/help'),
        KeyboardButton('/weather'),
        KeyboardButton('/news'),
    )
):
    try:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
        user = get_object_or_404(User, username=message.chat.username)
        answer = Answer.objects.create(
            recipient=user,
            command_response=Answer.Command.START
        )
        await message.reply(
            f'Привет {answer.recipient}. {answer.command_response}',
            reply_markup=keyboard
        )
    except Http404:
        await message.reply(PLEASE_REGISTER)
    except Exception as error:
        await message.reply(f'{UNKNOWN_ERROR} {error}')
        logger.warning(error)


@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    try:
        user = get_object_or_404(User, username=message.chat.username)
        answer = Answer.objects.create(
            recipient=user,
            command_response=Answer.Command.HELP
        )
        await message.reply(answer.command_response)
    except Http404:
        await message.reply(PLEASE_REGISTER)
    except Exception as error:
        await message.reply(f'{UNKNOWN_ERROR} {error}')
        logger.warning(error)


@dp.message_handler(commands=['news'])
async def get_news(message: Message):
    try:
        user = get_object_or_404(User, username=message.chat.username)
        date_timestamp, url, desc, title = parsing_news()
        answer = Answer.objects.create(
            recipient=user,
            description=desc,
            title=title,
            pub_date=timezone.make_aware(
                dt.fromtimestamp(date_timestamp) + datetime.timedelta(hours=4)
            ),
            link=url,
            command_response=Answer.Command.NEWS
        )
        await message.reply(
            f'{answer.command_response} \n {answer.pub_date} \n {answer.link}'
        )
    except Http404:
        await message.reply(PLEASE_REGISTER)
    except Exception as error:
        await message.reply(f'{UNKNOWN_ERROR} {error}')
        logger.warning(error)


@dp.message_handler(commands=['weather'])
async def get_city(
    message: Message,
    write_city='Напиши название города на англ в котором будем искать погоду'
):
    try:
        await message.reply(write_city)
    except Exception as error:
        await message.reply(f'{UNKNOWN_ERROR} {error}')
        logger.warning(error)


@dp.message_handler()
async def say_me_weather(message: Message):
    try:
        user = get_object_or_404(User, username=message.chat.username)
        weather = get_weather(message.text.split()[-1])
        answer = Answer.objects.create(
            recipient=user,
            city=weather.get('name'),
            temp=weather.get('main').get('temp'),
            humidity=weather.get('main').get('humidity'),
            sunrise=timezone.make_aware(
                dt.fromtimestamp(weather.get('sys').get('sunrise')) +
                datetime.timedelta(hours=7)
            ),
            command_response=Answer.Command.WEATHER
        )
        await message.reply(
            f'{answer.command_response} \n'
            f'В городе {answer.city} сейчас {answer.temp}°. \n'
            f'Влажность воздуха: {answer.humidity}. \n'
            f'Восход солнца: {answer.sunrise}. \n'
            f'\U00002620 Будь здоров:)'
        )
    except Http404:
        await message.reply(PLEASE_REGISTER)
    except Exception as error:
        await message.reply(f'{UNKNOWN_ERROR} {error}')
        logger.warning(error)


class Command(BaseCommand):
    help = 'Включение телеграмм бота'

    def handle(self, *args, **kwargs):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        django.setup()
        executor.start_polling(dp)
