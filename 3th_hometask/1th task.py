# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД.

from pymongo import MongoClient
import pickle


def func_write_to_mongo():
    # Переменная для хранения имени файла DataFrame
    file_df = f'df_vacancies.pickle'
    # Переменная для хранения имены базы данных MongoDB
    mongo_db_name = f'GB_parsing'
    # Переменная для хранения имены коллекции
    mongo_collection_name = f'vacancies'

    # Подключение к БД
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client[mongo_db_name]

    # Если БД не обнаружена
    if mongo_db_name not in mongo_client.list_database_names():
        # создать БД и коллекцию в ней
        mongo_db.create_collection(mongo_collection_name)

    # Чтение файла DataFrame с вакансиями
    with open(file=file_df, mode='rb') as file:
        df_vacancies = pickle.load(file=file)

    # Переменная для хранения списка столбцов DataFrame
    df_columns = list(df_vacancies.columns)

    # Для каждой строки DataFrame
    for i in range(df_vacancies.shape[0]):
        # добавить в коллекцию новую сущность с данными из DataFrame
        mongo_db[mongo_collection_name].insert_one({
            '_id': i,
            df_columns[0]: df_vacancies.loc[i][df_columns[0]],
            df_columns[1]: df_vacancies.loc[i][df_columns[1]],
            df_columns[2]: df_vacancies.loc[i][df_columns[2]],
            df_columns[3]: df_vacancies.loc[i][df_columns[3]],
            df_columns[4]: df_vacancies.loc[i][df_columns[4]],
            df_columns[5]: df_vacancies.loc[i][df_columns[5]],
            df_columns[6]: df_vacancies.loc[i][df_columns[6]],
            df_columns[7]: df_vacancies.loc[i][df_columns[7]]
        })

    mongo_client.close()


func_write_to_mongo()
