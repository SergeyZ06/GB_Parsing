import scrapy
from GB_parsing import items


class SpiderSuperjobSpider(scrapy.Spider):
    name = 'spider_superjob'
    # allowed_domains = ['https://www.superjob.ru/']
    # start_urls = ['http://https://www.superjob.ru//']
    vacancy = input(f'Enter vacancy for parsing on superjob.ru:\t')
    start_url = f'https://www.superjob.ru/vacancy/search/?keywords={vacancy}'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse_pages)

    def parse_pages(self, response):
        # Определение количества страниц с найденными вакансиями
        pages = response.xpath('//div[@class="_3zucV L1p51 _3ZDWc _2LZO7 iBQ9h GpoAF _3fOgw"]/a/span/span'
                               '/span[@class="_1BOkc"]/text()').extract()
        # Заведомо пустой результат поиска для дальнейшего сравнения
        pages_zero = response.xpath('//a[@class="fake_class_fake_class"]/text()').extract()
        url_current = response.request.url

        # Если результат поиска кол-ва страниц не пустой,
        # то для каждой страницы создать запрос
        if pages != pages_zero:
            pages_count = int(pages[len(pages) - 2])
            for page in range(pages_count):
                url = f'{url_current}?page={page + 1}'
                yield scrapy.Request(url=url, callback=self.parse_page)
        # иначе, начать поиск ссылок на вакансии на единственной странице
        else:
            for href in response.xpath('//div[@class="jNMYr GPKTZ _1tH7S"]/div[@class="_1h3Zg _2rfUm _2hCDz _21a7u"]'
                                       '/a/@href').extract():
                href_joined = response.urljoin(href)
                yield scrapy.Request(url=href_joined, callback=self.parse_vacancy)

    def parse_page(self, response):
        # На каждой открытой странице найти все ссылки на вакансии и создать запрос к ним
        print(response.request.url)
        for href in response.xpath('//div[@class="jNMYr GPKTZ _1tH7S"]/div[@class="_1h3Zg _2rfUm _2hCDz _21a7u"]'
                                   '/a/@href').extract():
            href_joined = response.urljoin(href)
            yield scrapy.Request(url=href_joined, callback=self.parse_vacancy)

    def parse_vacancy(self, response):
        # Для каждой страницы вакансии собрать необходимую информацию
        str_salary = response.xpath('//span[@class="_1OuF_ ZON4b"]/span/span[@class="_1h3Zg _2Wp8I _2rfUm _2hCDz"]'
                                    '/text()').extract()
        for i in range(len(str_salary)):
            str_salary[i] = str_salary[i].replace('\xa0', '').replace('руб.', '')

        if str_salary is not []:
            if str_salary[0] == 'от':
                salary_from = str_salary[2]
                salary_to = ''
            elif str_salary[0] == 'до':
                salary_from = ''
                salary_to = str_salary[2]
            else:
                salary_from = str_salary[0]
                salary_to = str_salary[1]
        else:
            salary_from = ''
            salary_to = ''

        yield items.GbParsingItem(
            title=response.xpath('//div[@class="_3MVeX"]/h1[@class="_1h3Zg rFbjy _2dazi _2hCDz"]'
                                 '/text()').extract_first(),
            salary_from=salary_from,
            salary_to=salary_to,
            link=response.request.url,
            source=fr'https://www.superjob.ru'
        )
