# 1. Доработать паука в имеющемся проекте, чтобы он складывал все записи в БД (любую) и
# формировал item по структуре:
# ● наименование вакансии;
# ● зарплата от;
# ● зарплата до;
# ● ссылка на саму вакансию;
# ● сайт, откуда собрана вакансия.
# 2. Создать в имеющемся проекте второго паука по сбору вакансий с сайта superjob. Паук должен
# формировать item по аналогичной структуре и складывать данные в БД.

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from GB_parsing import settings
from GB_parsing.spiders.spider_hhru import SpiderHhruSpider
from GB_parsing.spiders.spider_superjob import SpiderSuperjobSpider


if __name__ == '__main__':

    # Запуск Scrapy
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(crawler_or_spidercls=SpiderHhruSpider)
    process.crawl(crawler_or_spidercls=SpiderSuperjobSpider)
    process.start()

# Вакансии для отладки:
# Сантехник
# Слесарь
