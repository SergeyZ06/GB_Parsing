import scrapy
# from main import start_url as start_url_main
from GB_parsing import items


class SpiderHhruSpider(scrapy.Spider):
    name = 'spider_hhru'
    # allowed_domains = ['https://hh.ru', 'https://ruza.hh.ru']
    # start_urls = ['https://hh.ru/']
    # start_url = [start_url_main]
    vacancy = input(f'Enter vacancy for parsing on hh.ru:\t')
    start_url = f'https://ruza.hh.ru/search/vacancy?text={vacancy}'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse_pages)

    def parse_pages(self, response):
        # Определение количества страниц с найденными вакансиями
        pages = response.xpath('//div[@data-qa="pager-block"]/span/span/a[@class="bloko-button"]/span/text()').extract()
        pages_count = int(pages[len(pages) - 1])

        # Для каждой страницы создать запрос на её открытие
        for page in range(pages_count):
            url = fr'{response.request.url}&page={page}'
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        # На каждой открытой странице найти все ссылки на вакансии и создать запрос к ним
        for href in response.xpath('//span[@class="g-user-content"]/a[@class="bloko-link"]/@href').extract():
            yield scrapy.Request(url=href, callback=self.parse_vacancy)

    def parse_vacancy(self, response):
        # Для каждой страницы вакансии собрать необходимую информацию
        str_salary = response.xpath('//p[@class="vacancy-salary"]/span/text()').extract_first().strip().replace('\xa0', '')

        if str_salary.find(f'не указана') != -1:
            salary_from = ''
            salary_to = ''
        else:
            if str_salary.find(f'от') != -1:
                salary_from = str_salary.split()[1]
            else:
                salary_from = ''

            if str_salary.find('до') != -1:
                str_salary_splitted = str_salary.split()
                salary_to = str_salary_splitted[len(str_salary_splitted) - 2]
            else:
                salary_to = ''

        yield items.GbParsingItem(
            title=response.xpath('//h1[@data-qa="vacancy-title"]/text()').extract_first(),
            salary_from=salary_from,
            salary_to=salary_to,
            link=response.request.url,
            # source=self.allowed_domains[0]
            source=fr'https://hh.ru'
        )
