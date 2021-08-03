# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.

from pymongo import MongoClient


def func_search_in_mongo(salary):
    # Переменная для хранения имены базы данных MongoDB
    mongo_db_name = f'GB_parsing'
    # Переменная для хранения имены коллекции
    mongo_collection_name = f'vacancies'

    # Подключение к БД
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client[mongo_db_name]

    # Переменная для хранения запроса к БД
    mongo_query = {'$or': [{'salary_min': {'$gt': salary}}, {'salary_max': {'$gt': salary}}]}

    # Для каждой найденной записи
    for vacancy in mongo_db[mongo_collection_name].find(mongo_query):
        # вывести запись на экран
        print(vacancy)

    mongo_client.close()


func_search_in_mongo(salary=100000)
