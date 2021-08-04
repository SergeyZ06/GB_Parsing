# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient


class GbParsingPipeline:
    def process_item(self, item, spider):

        # Сохранение полученных Item в MongoDB
        mongo_db_name = f'GB_parsing'
        mongo_collection_name = f'scrapy_vacancies'

        mongo_client = MongoClient(host=f'localhost', port=27017)

        if mongo_client:
            mongo_db = mongo_client[mongo_db_name]

            if mongo_db_name not in mongo_client.list_database_names():
                mongo_db.create_collection(mongo_collection_name)

            mongo_db[mongo_collection_name].insert_one({
                'title':        item['title'],
                'salary_from':  item['salary_from'],
                'salary_to':    item['salary_to'],
                'link':         item['link'],
                'source':       item['source']
            })

            mongo_client.close()

        else:
            print(f'Error - MongoDB connection error!')

        return item
