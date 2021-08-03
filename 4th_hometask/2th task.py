# 2. Сложить собранные данные в БД

import pickle
from pymongo import MongoClient


# Функция для получения собранной информации из файлов
def func_load_from_pickle(file_name):
    with open(file=file_name, mode='rb') as file:
        list_news = pickle.load(file=file)
    return list_news


# Функция для записи информации в БД
def func_write_to_mongo(list_news):
    mongo_db_name = f'GB_parsing'
    mongo_collection_name = f'news'

    # Подключение к БД
    mongo_client = MongoClient(host='localhost', port=27017)
    mongo_db = mongo_client[mongo_db_name]

    # Проверка наличия БД, если БД отсутствует
    if mongo_db_name not in mongo_client.list_database_names():
        # то создать коллецию в указанной БД
        mongo_db.create_collection(mongo_collection_name)

    # Переменная для хранения списка полей коллекции
    collection_columns = list(list_news[0].keys())

    # Для каждой записи в списке новостей
    for i in range(len(list_news)):
        # вставить в коллекцию новую запись
        mongo_db[mongo_collection_name].insert_one({
            '_id':  i,
            collection_columns[0]:  list_news[i][collection_columns[0]],
            collection_columns[1]:  list_news[i][collection_columns[1]],
            collection_columns[2]:  list_news[i][collection_columns[2]],
            collection_columns[3]:  list_news[i][collection_columns[3]]
        })

    mongo_client.close()


file_mail = fr'data/mail.pickle'
file_lenta = fr'data/lenta.pickle'
file_yandex = fr'data/yandex.pickle'

# Получение списка новостей
list_news = []
list_news.extend(func_load_from_pickle(file_name=file_mail))
list_news.extend(func_load_from_pickle(file_name=file_lenta))
list_news.extend(func_load_from_pickle(file_name=file_yandex))

# Запись новостей в БД
func_write_to_mongo(list_news=list_news)
