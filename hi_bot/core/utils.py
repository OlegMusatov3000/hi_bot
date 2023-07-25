import time
from collections import Counter
from datetime import datetime as dt

import requests
from bs4 import BeautifulSoup


def parsing_news():
    url = 'https://www.securitylab.ru/news/'
    soup = BeautifulSoup(requests.get(url=url).text, 'lxml')

    news = soup.find('a', class_='article-card', id=True)

    url = f'https://www.securitylab.ru{news.get("href")}'
    title = news.find("h2").text.strip()
    desc = news.find("p").text.strip()
    date_from_iso = dt.fromisoformat(news.find('time').get('datetime'))
    date_time = dt.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')
    date_timestamp = time.mktime(
        dt.strptime(date_time, '%Y-%m-%d %H:%M:%S').timetuple()
    )

    return date_timestamp, url, desc, title


def get_favorite_command(objects):
    objects_list = [obj.get_command_response_display() for obj in objects]
    num_of_uses, fav_com = max(
        (count, value) for value, count in Counter(objects_list).items()
    )
    return num_of_uses, fav_com
