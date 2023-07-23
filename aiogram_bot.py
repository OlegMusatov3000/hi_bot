import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime as dt

import requests
from aiogram import Bot
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ParseMode
)
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

from parsing_news import get_last_news

load_dotenv()

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
    token=os.getenv('TOKEN'),
    parse_mode=ParseMode.HTML
)
dp = Dispatcher(bot)
API = os.getenv('API')
BUTTONS = (
    KeyboardButton('/start'),
    KeyboardButton('/help'),
    KeyboardButton('/weather [город]'),
    KeyboardButton('/news'),
)
COMMANDS = (
    '/start: Скажу привет и расскажу кратко, что умею,\n'
    '/help: Расскажу подробно какими командами ты можешь воспользоваться,\n'
    '/weather [город]: расскажу какая погода в этом городе,\n'
    '/news: ляяяя Галачка я те ща такое расскажу!!1!'
)


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*BUTTONS)
    start_massage = (
        f'Привет 👋, {message.chat.first_name}!\n'
        'Я бот который родился в процессе написания тестового задания.\n'
        'Расскажу интересные новости и скажу какая погода в твоем городе.\n'
        'Cписок рабочих команд ты увидешь заюзая команду: /help\n'
        'Надеюсь тебе понравится:)'
    )
    await message.reply(start_massage, reply_markup=keyboard)
    logger.warning(start_massage)


@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    await message.reply(COMMANDS)
    logger.warning(COMMANDS)


@dp.message_handler(commands=['weather'])
async def get_city(message: Message):
    await message.reply(
        'Напиши название города на английском в котором будем искать погоду'
    )


@dp.message_handler()
async def get_weather(message: Message):
    try:
        r = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?q=\n'
            f'{message.text.split()[-1]}&appid={API}&units=metric'
        )
        data = r.json()
        answer_massage = (
            f'В городе {data["name"]} сейчас {data["main"]["temp"]}°.\n'
            f'Влажность воздуха: {data["main"]["humidity"]}.\n'
            f'Восход солнца: {dt.fromtimestamp(data["sys"]["sunrise"])}.\n'
            f'\U00002620 Будь здоров:)'
        )
        await message.reply(answer_massage)
        logger.warning(answer_massage)

    except Exception:
        error = (
            '\U00002620 Проверь название города, бро:)\n'
            'Мб ты пишешь на русском или с ошибками или вообще не указал?'
        )
        await message.reply(error)
        logger.warning(error)


@dp.message_handler(commands=['news'])
async def get_news(message: Message):
    date_timestamp, url = get_last_news()
    news = f'<b>{dt.fromtimestamp(date_timestamp)}</b> {url}'
    await message.reply(news)
    return logger.warning(news)


if __name__ == '__main__':
    executor.start_polling(dp)
