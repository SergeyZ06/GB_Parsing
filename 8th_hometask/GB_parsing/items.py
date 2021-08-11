import scrapy
from itemloaders.processors import MapCompose
from itemloaders.processors import TakeFirst


# Процессор для обработки цены товара
def filter_price(value):
    result = value.replace(' ', '')
    if result.isdigit():
        return int(result)


# Процессор для обработки заголовка товара
def filter_title(value):
    return value.strip()


# Процессор для обработки характеристик товара
def filter_characteristics(value):
    processed_dict = {}
    # Если характеристики товара присутствуют
    if len(value) > 0:
        # то обработать название каждой характеристики и её значение:
        # удалить все лишние пробелы и переносы строк
        for key in value.keys():
            new_key = str(key).strip()
            new_value = str(value[key]).strip()
            processed_dict[new_key] = new_value
    return processed_dict.copy()


class GbParsingItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(filter_title),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(filter_price),
        output_processor=TakeFirst()
    )
    characteristics = scrapy.Field(
        input_processor=MapCompose(filter_characteristics)
    )
    image_urls = scrapy.Field()
    images = scrapy.Field()
