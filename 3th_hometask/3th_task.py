# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

import pymongo
from pymongo import MongoClient
import pickle


def func_add_new_records_to_mongo():
    # Переменная для хранения имени файла DataFrame
    file_df = f'df_vacancies.pickle'
    # Переменная для хранения имены базы данных MongoDB
    mongo_db_name = f'GB_parsing'
    # Переменная для хранения имены коллекции
    mongo_collection_name = f'vacancies'

    # Подключение к БД
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client[mongo_db_name]

    # Чтение файла DataFrame с вакансиями
    with open(file=file_df, mode='rb') as file:
        df_vacancies = pickle.load(file=file)

    # Переменная для хранения списка столбцов DataFrame
    df_columns = list(df_vacancies.columns)

    # Для каждой строки DataFrame
    for i in range(df_vacancies.shape[0]):
        mongo_query = {
            df_columns[0]: df_vacancies.loc[i][df_columns[0]],
            df_columns[1]: df_vacancies.loc[i][df_columns[1]],
            df_columns[2]: df_vacancies.loc[i][df_columns[2]],
            df_columns[3]: df_vacancies.loc[i][df_columns[3]],
            df_columns[4]: df_vacancies.loc[i][df_columns[4]],
            df_columns[5]: df_vacancies.loc[i][df_columns[5]],
            df_columns[6]: df_vacancies.loc[i][df_columns[6]],
            df_columns[7]: df_vacancies.loc[i][df_columns[7]]
        }

        # Если строка не обнаружена в БД
        if len(list(mongo_db[mongo_collection_name].find(mongo_query))) == 0:
            # определить максимальный _id среди всех документов коллекции
            max_id = mongo_db[mongo_collection_name].find({}, sort=[('_id', pymongo.DESCENDING)])[0]['_id']

            # добавить в коллекцию ненайденный документ с очередным _id
            mongo_db[mongo_collection_name].insert_one({
                '_id': max_id + 1,
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


func_add_new_records_to_mongo()
