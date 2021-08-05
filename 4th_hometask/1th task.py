# 1. Написать приложение, которое собирает основные новости с сайтов
# ● https://news.mail.ru,
# ● https://lenta.ru,
# ● https://yandex.ru/news.
# Для парсинга использовать XPath. Структура данных должна содержать:
# ● название источника;
# ● наименование новости;
# ● ссылку на новость;
# ● дата публикации.

from fake_headers import Headers
from lxml import html
import requests
import time
import datetime
import pickle
import random


# Функция для парсинга новостей mail.ru
def func_parsing_mail(url):
    list_news = []
    header = Headers(headers=True).generate()

    response = requests.get(url=url, headers=header)

    # Если удалось получить ответ
    if response:
        # преобразовать ответ в html документ
        root = html.fromstring(response.text)

        # получить список ссылок новостей по указанному xpath
        list_links = root.xpath(r'//a[@class="list__text"]/@href')
        # получить список заголовков новостей по указанному xpath
        list_titles = root.xpath(r'//a[@class="list__text"]')

        # Даты и источники новостей получить по ссылкам на новости
        list_dates = []
        list_sources = []
        for link in list_links:
            time.sleep(2)
            root_item = html.fromstring(requests.get(url=link, headers=header).text)
            list_dates.append(root_item.xpath(r'//span[@class="note__text breadcrumbs__text js-ago"]/@datetime'))
            list_sources.append(root_item.xpath(r'//span[@class="note"]/a[@class="link color_gray breadcrumbs__link"]/'
                                                r'@href'))

        # Собранную информацию о каждой новости записать в список в виде словаря
        for item_list in range(len(list_links)):
            list_news.append({
                'source':   list_sources[item_list][0],
                'title':    list_titles[item_list].text.replace('\xa0', ' '),
                'link':     list_links[item_list],
                'date':     list_dates[item_list][0]
            })

        return list_news


# Функция для парсинга новостей lenta.ru
def func_parsing_lenta(url):
    list_news = []
    header = Headers(headers=True).generate()

    response = requests.get(url=url, headers=header)

    if response:
        root = html.fromstring(response.text)

        list_titles = root.xpath(r'//*[@id="root"]/section[2]/div/div/div[1]/section[1]/div/div[@class="item"]/a/'
                                 r'text()')

        list_links = root.xpath(r'//*[@id="root"]/section[2]/div/div/div[1]/section[1]/div/div[@class="item"]/a/@href')

        list_dates = root.xpath(r'//*[@id="root"]/section[2]/div/div/div[1]/section[1]/div/div[@class="item"]/a/'
                                r'time/@datetime')

        for item_list in range(len(list_links)):
            # Если ссылка на новость не начинается с символов 'http',
            # то значит это собственная новость lenta.ru
            # и в поле source будет записана ссылка на сам агрегатор новостей
            def lambda_source(x): return fr'{x.split("/")[0]}//{x.split("/")[2]}/' if x[0:4] == fr'http' else url

            # Если ссылка на новость не начинается с символов 'http',
            # то значит это внутреняя ссылка агрегатора lenta.ru.
            # Например:
            # /news/2021/08/04/health_covid/'
            # должно быть преобразовано в:
            # https://lenta.ru/news/2021/08/04/health_covid/
            def lambda_url(x): return x if x[0:4] == fr'http' else fr'{url[:-1]}{x}'

            list_news.append({
                'source':   lambda_source(list_links[item_list]),
                'title':    list_titles[item_list].replace('\xa0', ' '),
                'link':     lambda_url(list_links[item_list]),
                'date':     list_dates[item_list]
            })

        return list_news


# Функция для парсинга новостей yandex.ru
def func_parsing_yandex(url):
    list_news = []
    header = Headers(headers=True).generate()

    response = requests.get(url=url, headers=header)

    if response:
        root = html.fromstring(response.text)

        list_titles = root.xpath(r'//div[@class="mg-card__text"]/a[@class="mg-card__link"]/h2[@class="mg-card__title"]'
                                 r'/text()')

        list_links = root.xpath(r'//div[@class="mg-card__text"]/a[@class="mg-card__link"]/@href')

        list_dates = root.xpath(r'//div/article/div/div/div/span[@class="mg-card-source__time"]/text()')
        current_date = datetime.date.today()

        list_sources = []
        for link in list_links:
            # Скрапинг каждого источника новостей осуществляется с задержкой
            # и с новым User Agent в целях предотвращения блокировки со стороны Yandex.ru
            random_sleep = random.randint(0, 90)
            time.sleep(90 + random_sleep)
            header_item = Headers(headers=True).generate()
            root_item = html.fromstring(requests.get(url=link, headers=header_item).text)
            list_sources.append(root_item.xpath(r'//div[@class="news-story__head"]/a[@class="news-story__subtitle"]'
                                                r'/@href'))
            # print(list_sources[len(list_sources) - 1])

        for item_list in range(len(list_titles)):
            # Если yandex.ru перестал выдавать response,
            # то записать в поле source пустую строку
            def lambda_source(x): return x[0] if len(x) > 0 else ''

            list_news.append({
                'source':   lambda_source(list_sources[item_list]),
                'title':    list_titles[item_list].replace('\xa0', ' '),
                'link':     list_links[item_list],
                'date':     fr'{current_date} {list_dates[item_list]}'
            })

        return list_news


# Функция для записи собранных новостей в файл
def func_to_pickle(list_news, file_name, check=False):
    with open(file=file_name, mode='wb') as file:
        pickle.dump(obj=list_news, file=file)
    # проверка записанных новостей
    if check is True:
        with open(file=file_name, mode='rb') as file:
            list_news = pickle.load(file=file)
        for item in list_news:
            print(item)


url_mail = fr'https://news.mail.ru/'
file_mail = fr'data/mail.pickle'

url_lenta = fr'https://lenta.ru/'
file_lenta = fr'data/lenta.pickle'

url_yandex = fr'https://yandex.ru/news'
file_yandex = fr'data/yandex.pickle'

# Парсинг и запись в файл новостей mail.ru
list_news_mail = func_parsing_mail(url=url_mail)
func_to_pickle(list_news=list_news_mail, file_name=file_mail, check=True)

# Парсинг и запись в файл новостей lenta.ru
list_news_lenta = func_parsing_lenta(url=url_lenta)
func_to_pickle(list_news=list_news_lenta, file_name=file_lenta, check=True)

# Парсинг и запись в файл новостей yandex.ru
list_news_yandex = func_parsing_yandex(url=url_yandex)
func_to_pickle(list_news=list_news_yandex, file_name=file_yandex, check=True)
