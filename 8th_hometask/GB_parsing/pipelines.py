import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pathlib import Path
import datetime
import csv


# Pipeline для обработки общей информации о товарах
class GbParsingPipeline:
    @staticmethod
    def process_item(item, spider):
        # Формирование отчёта о парсинге:
        # временная метка операции
        str_to_file = str(datetime.datetime.now())

        # наименование товара
        str_title = item['title']
        str_to_file += str('\n' + str_title)

        # стоимость товара
        str_price = f'Стоимость: {item["price"]}'
        str_to_file += str('\n' + str_price)

        # характеристики товара
        for key in item['characteristics'][0].keys():
            str_characteristics = f'{key}: {item["characteristics"][0][key]}'
            str_to_file += str('\n' + str_characteristics)

        # информация о фото товара
        if item['image_urls']:
            str_to_file += str('\n' + f'Фото:')
            for image_url in item['image_urls']:
                url = image_url
                url_splitted = url.split('/')
                file_name = url_splitted[len(url_splitted) - 1]
                str_file_name = f'\t{file_name}'
                str_to_file += str('\n' + str_file_name)

        # Вывод отчёта на экран
        print(f'\n + {str_to_file}')

        # Файл для записи отчёта
        path_result_txt = Path(r'result.txt')

        # Запись отчёта в файл
        if path_result_txt.exists():
            with open(file=path_result_txt, mode='a') as file_result_txt:
                file_result_txt.write('\n')
                file_result_txt.write('\n')
                file_result_txt.write('\n')
                file_result_txt.write(str_to_file.replace('\xb2', '2'))
        else:
            with open(file=path_result_txt, mode='w') as file_result_txt:
                file_result_txt.write(str_to_file.replace('\xb2', '2'))

        return item


# Pipeline для обработки фото товаров
class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # Если item содержит информацию о фото товара
        if item['image_urls']:
            # обработать каждое фото
            for image_url in item['image_urls']:
                try:
                    yield scrapy.Request(url=image_url)
                except Exception as exc:
                    print(exc)

    def item_completed(self, results, item, info):
        if results:
            item['images'] = [itm[1] for itm in results if itm[0]]
            return item

    def file_path(self, request, response=None, info=None, *, item=None):
        # Получения имени файла из ссылки на файл
        url = request.url
        url_splitted = url.split('/')
        path = url_splitted[len(url_splitted) - 1]
        return path


# Pipeline для записи в csv общей информации о товарах
class MyCSVPipeline:
    def __init__(self):
        # Файл для записи csv
        self.path_result_csv = Path(r'result.csv')

        # Если файл существует
        if self.path_result_csv.exists():
            # открыть файл
            with open(file=self.path_result_csv, mode='r', newline='') as file_result_csv:
                # получить список заголовков полей
                self.tmp_data = csv.DictReader(file_result_csv).fieldnames
        # Если файл не существует
        else:
            # создать файл
            with open(file=self.path_result_csv, mode='w', newline=''):
                # установить флаг, что файл не содержит заголовков полей
                self.tmp_data = None

        self.file_result_csv = open(file=self.path_result_csv, mode='a', newline='', encoding='UTF-8')

    def process_item(self, item, spider):
        # Получить список полей из item
        columns = item.fields.keys()

        # обратится к файлу csv для записи информации
        data = csv.DictWriter(self.file_result_csv, columns)

        # Если заголовки в файле отсутствуют
        if not self.tmp_data:
            # записать заголовки в файл
            data.writeheader()
            # установить флаг, что файл содержит заголовки
            self.tmp_data = True

        # Записать в файл информацию об item
        data.writerow(item)
        return item

    def __del__(self):
        self.file_result_csv.close()
