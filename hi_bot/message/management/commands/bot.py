import os
import sys
import logging

import django
from aiogram import Bot
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from django.http import Http404
from django.core.management.base import BaseCommand

from hi_bot.settings import TOKEN
from core.utils import parsing_news, get_weather, create_message
from message.models import Answer
from message.constants import PLEASE_REGISTER, UNKNOWN_ERROR


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
        answer = create_message(Answer.Command.START, message.chat.username)
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
        answer = create_message(
            command=Answer.Command.HELP,
            username=message.chat.username
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
        pub_date, url, description, title = parsing_news()
        answer = create_message(
            command=Answer.Command.NEWS,
            username=message.chat.username,
            description=description,
            title=title,
            pub_date=pub_date,
            link=url
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
        city, temp, humidity, sunrise = get_weather(message.text.split()[-1])
        answer = create_message(
            command=Answer.Command.WEATHER,
            username=message.chat.username,
            city=city,
            temp=temp,
            humidity=humidity,
            sunrise=sunrise
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
