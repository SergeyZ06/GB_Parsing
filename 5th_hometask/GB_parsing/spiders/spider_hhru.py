import scrapy
from GB_parsing import items


class SpiderHhruSpider(scrapy.Spider):
    name = 'spider_hhru'
    # allowed_domains = ['https://hh.ru', 'https://ruza.hh.ru']
    # start_urls = ['https://hh.ru/']
    vacancy = input(f'Enter vacancy for parsing on hh.ru:\t')
    start_url = f'https://ruza.hh.ru/search/vacancy?text={vacancy}'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse_pages)

    def parse_pages(self, response):
        # Определение количества страниц с найденными вакансиями
        pages = response.xpath('//div[@data-qa="pager-block"]/span/span/a[@class="bloko-button"]/span/text()').getall()

        # Если результат поиска кол-ва страниц не пустой,
        # то для каждой страницы создать запрос
        if len(pages) != 0:
            pages_count = int(pages[len(pages) - 1])
            for page in range(pages_count):
                url = fr'{response.request.url}&page={page}'
                yield scrapy.Request(url=url, callback=self.parse_page)
        # иначе, начать поиск ссылок на вакансии на единственной странице
        else:
            for href in response.xpath('//span[@class="g-user-content"]/a[@class="bloko-link"]/@href').getall():
                yield scrapy.Request(url=href, callback=self.parse_vacancy)

    def parse_page(self, response):
        # На каждой открытой странице найти все ссылки на вакансии и создать запрос к ним
        for href in response.xpath('//span[@class="g-user-content"]/a[@class="bloko-link"]/@href').getall():
            yield scrapy.Request(url=href, callback=self.parse_vacancy)

    def parse_vacancy(self, response):
        # Для каждой страницы вакансии собрать необходимую информацию
        # str_salary = response.xpath('//p[@class="vacancy-salary"]/span/text()').get().strip().replace('\xa0', '')
        str_salary = response.xpath('//div[@class="vacancy-title"]/p/span/text()').get()

        if str_salary is None:
            salary_from = ''
            salary_to = ''
        else:
            str_salary = str_salary.strip().replace('\xa0', '')
            if len(str_salary) != 0:
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
            else:
                salary_from = ''
                salary_to = ''

        yield items.GbParsingItem(
            title=response.xpath('//h1[@data-qa="vacancy-title"]/text()').get(),
            salary_from=salary_from,
            salary_to=salary_to,
            link=response.request.url,
            source=fr'https://hh.ru'
        )
