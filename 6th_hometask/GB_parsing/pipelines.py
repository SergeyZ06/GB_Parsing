import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pathlib import Path
import datetime


class GbParsingPipeline:
    def process_item(self, item, spider):
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
        if len(item['characteristics']) % 2 == 0:
            # характеристики товара предствляют собой список
            # первая половина списка - это названия характеристик
            # вторая половина - значения характеристик
            len_2 = int(len(item['characteristics']) / 2)
            for i in range(len_2):
                # для удобства восприятия характеристики и их значения выводятся в одной строке
                str_characteristics = f'{item["characteristics"][i]}: {item["characteristics"][i + len_2]}'
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
        file_result = Path(r'result.txt')

        # Запись отчёта в файл
        if file_result.exists():
            with open(file=file_result, mode='a') as file:
                file.write('\n')
                file.write('\n')
                file.write(str_to_file.replace('\xb2', '2'))
        else:
            with open(file=file_result, mode='w') as file:
                file.write(str_to_file.replace('\xb2', '2'))

        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['image_urls']:
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
