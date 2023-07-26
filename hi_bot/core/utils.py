import time
from datetime import datetime as dt

import requests
from bs4 import BeautifulSoup as bt

from hi_bot.settings import NEWS_URL, WEATHER_URL, API_WEATHER


def parsing_news():
    soup = bt(requests.get(NEWS_URL + '/news/').text, 'lxml')

    news = soup.find('a', class_='article-card', id=True)

    url = NEWS_URL + news.get("href")
    title = news.find("h2").text.strip()
    desc = news.find("p").text.strip()
    date_from_iso = dt.fromisoformat(news.find('time').get('datetime'))
    date_time = dt.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')
    date_timestamp = time.mktime(
        dt.strptime(date_time, '%Y-%m-%d %H:%M:%S').timetuple()
    )

    return date_timestamp, url, desc, title


def get_weather(city):
    return (
        requests.get(
            f'{WEATHER_URL}data/2.5/weather?q={city}'
            f'&appid={API_WEATHER}&units=metric'
        ).json()
    )
