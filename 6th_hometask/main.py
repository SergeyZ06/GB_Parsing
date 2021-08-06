# 3. Взять любую категорию товаров на сайте Леруа Мерлен. Собрать с использованием
# ItemLoader следующие данные:
# ● название;
# ● все фото;
# ● параметры товара в объявлении.
# 4. С использованием output_processor и input_processor реализовать очистку и преобразование
# данных. Цены должны быть в виде числового значения.


from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from GB_parsing import settings
from GB_parsing.spiders.spider_paints import SpiderPaintsSpider


if __name__ == '__main__':

    # Запуск Scrapy
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(crawler_or_spidercls=SpiderPaintsSpider)
    process.start()
