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
import pandas as pd

file_df = f'df_vacancies.pickle'
df_columns = [f'name',
              f'salary_min',
              f'salary_max',
              f'money_currency',
              f'vacancy_url',
              f'service_url',
              f'company',
              f'location']
df_vacancies = pd.DataFrame(columns=df_columns)

vacancy_search = input(f'Type vacancy title for looking for:\t')
if vacancy_search == '':
    print(f'Error: empty value has been given!')
    exit()

vacancy_pages = input(f'Specify amount of pages from one up to five, one is default value:\t')

# Проверка на корректность ввёденного значения страниц
try:
    vacancy_pages = int(vacancy_pages)
except ValueError:
    print(f'Error - incorrect value of amount of pages:\t{vacancy_pages}\nIt should be integer value!')
    exit()

if (vacancy_pages < 1) or (vacancy_pages > 5):
    print(f'Error: incorrect value of amount of pages:\t{vacancy_pages}\nIt should be between one and five!')
    exit()

header = Headers(headers=True).generate()


# Скрапинг и парсинг hh.ru
url_hh = r'https://hh.ru/search/vacancy?text='
url_hh = url_hh + vacancy_search

for page_number in range(vacancy_pages):
    url_hh_current = url_hh + fr'&page={page_number}'
    response = requests.get(url=url_hh_current, headers=header).text

    # Сперва происходит поиск всех элементов html, содержащих информацию о вакансиях
    bs_hh_page = BeautifulSoup(response, f'lxml')
    vacancies = bs_hh_page.find_all(class_=f'vacancy-serp-item')

    # Затем проводится разбор каждого блока
    for text in vacancies:
        # Список параметров вакансии
        list_vacancy = []
        text = str(text)
        bs_hh_vacancy = BeautifulSoup(text, f'lxml')

        # Наименование вакансии
        list_vacancy.append(bs_hh_vacancy.find(name=f'a', class_=f'bloko-link').text)

        # Зарплата
        # Разбиение строки с зарплатой на слова
        list_salary = bs_hh_vacancy.find(name=f'div', class_=f'vacancy-serp-item__sidebar').text.\
            replace(f'\u202f', f'').split()
        # Для каждого слова в этой строке
        for str_salary in list_salary:
            # установить флаг ошибки = 0
            flag_value_error = 0
            # пробовать преобразовать слово в число
            try:
                str_salary = int(str_salary)
            except ValueError:
                # если не получается, то поднять флаг ошибки = 1
                flag_value_error = 1
            finally:
                # каждое слово, успешно преобразованное в число, записать в список параметров вакансии
                if flag_value_error == 0:
                    list_vacancy.append(str_salary)

            # В случае анализа последнего слова строки
            if str_salary == list_salary[len(list_salary) - 1]:
                # если длина списка параметров вакансии = 2, значит в список не попала максимальная цена
                if len(list_vacancy) == 2:
                    # добавить прочерк на место максимальной цены
                    list_vacancy.append('-')
                # добавить в список параметров вакансии валюту зарплаты
                list_vacancy.append(str_salary)
        # Если информация о зарплате не обнаружена, то соответствующие поля заполняются прочерками
        if len(list_vacancy) == 1:
            list_vacancy.append(f'-')
            list_vacancy.append(f'-')
            list_vacancy.append(f'-')

        # Ссылка на вакансию
        list_vacancy.append(bs_hh_vacancy.find(name=f'a', class_=f'bloko-link')[f'href'])

        # Сайт, откуда собрана вакансия.
        url_str = ''
        url_list = list_vacancy[len(list_vacancy) - 1].split('/')
        for i in range(3):
            url_str += url_list[i] + '/'
        list_vacancy.append(url_str)

        # Работодатель
        list_vacancy.append(bs_hh_vacancy.find(name=f'div', class_=f'vacancy-serp-item__meta-info-company').text.
                            replace('\xa0', f' '))

        # Расположение
        list_vacancy.append(bs_hh_vacancy.find(name=f'span', class_=f'vacancy-serp-item__meta-info').text)

        # Запись сформированного списка в dataframe
        series_vacancy = pd.Series(list_vacancy, index=df_columns)
        df_vacancies = df_vacancies.append(series_vacancy, ignore_index=True)


# Скрапинг и парсинг SuperJob
url_superjob = r'https://www.superjob.ru/vacancy/search/?keywords='
url_superjob = url_superjob + vacancy_search

for page_number in range(vacancy_pages):
    if page_number == 0:
        response = requests.get(url=url_superjob, headers=header)
        url_superjob = response.url
    else:
        url_superjob_current = url_superjob + f'?page={page_number + 1}'
        response = requests.get(url=url_superjob_current, headers=header)

    # Сперва происходит поиск всех элементов html, содержащих информацию о вакансиях
    bs_superjob_page = BeautifulSoup(response.text, f'lxml')
    vacancies = bs_superjob_page.find_all(name=f'div', class_=f'_31XDP iJCa5 f-test-vacancy-item _1fma_ _2nteL')

    # Затем проводится разбор каждого блока
    for text in vacancies:
        # Список параметров вакансии
        list_vacancy = []
        text = str(text)
        bs_superjob_vacancy = BeautifulSoup(text, f'lxml')

        # Наименование вакансии
        list_vacancy.append(bs_superjob_vacancy.find(name=f'div', class_=f'_1h3Zg _2rfUm _2hCDz _21a7u').text)

        # Зарплата
        list_salary = bs_superjob_vacancy.find(name=f'span', class_=f'_1h3Zg _2Wp8I _2rfUm _2hCDz _2ZsgW').text.\
            replace(f'\xa0', f' ').split()
        if list_salary[0] == f'от':
            list_vacancy.append(int(list_salary[1] + list_salary[2]))
            list_vacancy.append(f'-')
            list_vacancy.append(list_salary[len(list_salary) - 1])
        elif list_salary[0] == f'до':
            list_vacancy.append(f'-')
            list_vacancy.append(int(list_salary[1] + list_salary[2]))
            list_vacancy.append(list_salary[len(list_salary) - 1])
        elif (list_salary[0] == f'По') and (list_salary[1] == f'договорённости'):
            list_vacancy.append(f'-')
            list_vacancy.append(f'-')
            list_vacancy.append(f'-')
        elif list_salary[2] == f'-':
            list_vacancy.append(int(list_salary[1] + list_salary[2]))
            list_vacancy.append(int(list_salary[3] + list_salary[4]))
            list_vacancy.append(list_salary[len(list_salary) - 1])
        elif list_salary[2] == f'—':
            list_vacancy.append(int(list_salary[0] + list_salary[1]))
            list_vacancy.append(int(list_salary[3] + list_salary[4]))
            list_vacancy.append(list_salary[len(list_salary) - 1])
        else:
            list_vacancy.append(int(list_salary[0] + list_salary[1]))
            list_vacancy.append(int(list_salary[0] + list_salary[1]))
            list_vacancy.append(list_salary[len(list_salary) - 1])

        # Ссылка на вакансию
        list_vacancy.append(fr'https://superjob.ru' + bs_superjob_vacancy.find(name=f'a', class_=f'icMQ_')[f'href'])

        # Сайт, откуда собрана вакансия.
        url_str = ''
        url_list = list_vacancy[len(list_vacancy) - 1].split('/')
        for i in range(3):
            url_str += url_list[i] + '/'
        list_vacancy.append(url_str)

        # Работодатель
        employer = bs_superjob_vacancy.find(name=f'a', class_=f'_205Zx')
        if employer:
            list_vacancy.append(employer.text)
        else:
            list_vacancy.append(f'-')

        # Расположение
        list_vacancy.append(bs_superjob_vacancy.find(name=f'span', class_=f'f-test-text-company-item-location').text.
                            split(f' • ')[1])

        # Запись сформированного списка в dataframe
        series_vacancy = pd.Series(list_vacancy, index=df_columns)
        df_vacancies = df_vacancies.append(series_vacancy, ignore_index=True)

# Сохранение полученного DataFrame
with open(file=file_df, mode='wb') as file:
    pickle.dump(obj=df_vacancies, file=file)

# Проверка сохранённого DataFrame
with open(file=file_df, mode='rb') as file:
    df_vacancies = pickle.load(file=file)

print(df_vacancies)
