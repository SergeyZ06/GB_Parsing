# Вариант 1
# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
# Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия. ### По желанию можно добавить ещё параметры вакансии (например, работодателя и
# расположение). Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью
# dataFrame через pandas.

import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import pickle

# url_hh = r'https://hh.ru/search/vacancy?text='
# url_hh = r'https://hh.ru/search/vacancy?text=%D0%A1%D0%B0%D0%BD%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B8'

# header = Headers(headers=True)
# response = requests.get(url=url_hh, headers=header.generate()).text

# with open(file=r'hh.pickle', mode='wb') as file:
#     pickle.dump(obj=response, file=file)

with open(file='hh.pickle', mode='rb') as file:
    response = pickle.load(file=file)

bs = BeautifulSoup(response, 'lxml')

vacancies = bs.find_all(class_='vacancy-serp-item')
# print(str(vacancies[0]).split(r'target="_blank">')[1].split(r'</a></span></span></span></div><div class="vacancy-serp
# -item__sidebar">')[0])
print(vacancies[0])

for text in vacancies:
    print(str(text).split(r'target="_blank">')[1].split(
        r'</a></span></span></span></div><div class="vacancy-serp-item__sidebar">')[0])
