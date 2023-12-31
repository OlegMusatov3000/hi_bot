'''В этом модуле собраны все вспомогательные функции приложения "hi_bot".'''
import time
import datetime as dt

import requests
from bs4 import BeautifulSoup as bt
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator

from message.models import User, Answer
from hi_bot.settings import NEWS_URL, WEATHER_URL, API_WEATHER


def paginate(request, objects, count=10):
    '''
    Выводит объекты переданные в переменную постранично. Количество объектов
    на одной странице указанно по умолчанию в переменную "count".
    '''
    return Paginator(objects, count).get_page(request.GET.get('page'))


def parsing_news():
    '''Возвращает самую свежую новость сайта https://www.securitylab.ru.'''
    soup = bt(requests.get(NEWS_URL + '/news/').text, 'lxml')

    news = soup.find('a', class_='article-card', id=True)

    url = NEWS_URL + news.get("href")
    title = news.find("h2").text.strip()
    description = news.find("p").text.strip()
    date_from_iso = dt.datetime.fromisoformat(
        news.find('time').get('datetime')
    )
    date_time = dt.datetime.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')
    date_timestamp = time.mktime(
        dt.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').timetuple()
    )
    pub_date = timezone.make_aware(
        dt.datetime.fromtimestamp(date_timestamp)
    )

    return pub_date, url, description, title,


def get_weather(city):
    '''
    Возвращает погоду в указанном городе.
    Ожидает на вход город для определения погоды.
    '''
    weather_data = requests.get(
        f'{WEATHER_URL}data/2.5/weather?q={city}'
        f'&appid={API_WEATHER}&units=metric'
    ).json()
    city = weather_data.get('name')
    temp = weather_data.get('main').get('temp')
    humidity = weather_data.get('main').get('humidity')
    sunrise = timezone.make_aware(
        dt.datetime.fromtimestamp(weather_data.get('sys').get('sunrise'))
    )
    return city, temp, humidity, sunrise


def create_message(
    command,
    username,
    description=None,
    title=None,
    pub_date=None,
    link=None,
    city=None,
    temp=None,
    humidity=None,
    sunrise=None
):
    '''
    Создает объект "Answer" с полями переданными в данный метод.
    '''
    user = get_object_or_404(User, username=username)
    answer = Answer.objects.create(
        recipient=user,
        command_response=command,
        description=description,
        title=title,
        pub_date=pub_date,
        link=link,
        city=city,
        temp=temp,
        humidity=humidity,
        sunrise=sunrise
    )
    return answer
