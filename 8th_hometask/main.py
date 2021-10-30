# 1. В ранее написанное приложение добавить класс с функциями, которые позволят собрать
# открытые данные по выбранной теме при помощи Python с сайта (выберите из списка
# известных источников данных)


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
