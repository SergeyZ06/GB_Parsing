import scrapy
from itemloaders.processors import MapCompose
from itemloaders.processors import TakeFirst


# Процессор для обработки цены товара
def filter_price(value):
    result = value.replace(' ', '')
    if result.isdigit():
        return int(result)


# Процессор для обработки текстовых полей товара
def filter_text(value):
    if type(value) == str:
        return value.strip()


class GbParsingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field(
        input_processor=MapCompose(filter_text),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(filter_price),
        output_processor=TakeFirst()
    )
    characteristics = scrapy.Field(
        input_processor=MapCompose(filter_text)
    )

    image_urls = scrapy.Field()
    images = scrapy.Field()
