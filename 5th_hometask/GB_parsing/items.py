# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GbParsingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # Поля вакансии для парсинга
    title = scrapy.Field()
    salary_from = scrapy.Field()
    salary_to = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
    pass
