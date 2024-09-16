import scrapy
from urllib.parse import urljoin
from GB_parsing.items import GbParsingItem
from scrapy.loader import ItemLoader


class SpiderPaintsSpider(scrapy.Spider):
    name = 'spider_paints'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/kraski-dlya-vnutrennih-rabot/']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse_pages)

    def parse_pages(self, response):
        # Получение кол-ва страниц товаров
        pages_count = response.xpath('//div[@aria-label="Pagination"]/div/div/a/span[@class="cef202m_plp"]'
                                    '/text()').get()

        if pages_count.isdigit():
            pages_count = int(pages_count)
            for page in range(pages_count):
                # Получение ссылки на страницу каталога товаров
                url = urljoin(response.request.url, fr'?page={page + 1}')
                yield scrapy.Request(url=url, callback=self.parse_page)

        else:
            # Если кнопки переключения страниц каталога товаров не найдены,
            # то значит, что страница одна
            yield scrapy.Request(url=response.request.url, callback=self.parse_page)

    def parse_page(self, response):
        # Получение ссылок на товары
        list_urls = response.xpath('//a[@class="bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp"]/@href').getall()

        if len(list_urls) > 0:
            for url in list_urls:
                url = urljoin(f'https://leroymerlin.ru', url)
                yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        # Сбор информации о товаре:
        my_item_loader = ItemLoader(item=GbParsingItem(), response=response)
        # наименование
        my_item_loader.add_xpath(field_name='title', xpath='//h1[@slot="title"]/text()')
        # стоимость
        my_item_loader.add_xpath(field_name='price', xpath='//uc-pdp-price-view[@class="primary-price"]'
                                                           '/span[@slot="price"]/text()')
        # названия полей характеристик товара
        my_item_loader.add_xpath(field_name='characteristics', xpath='//dl[@class="def-list"]'
                                                                     '/div[@class="def-list__group"]/dt/text()')
        # значения полей характеристик товара
        my_item_loader.add_xpath(field_name='characteristics', xpath='//dl[@class="def-list"]'
                                                                     '/div[@class="def-list__group"]/dd/text()')
        # ссылки на фото товара
        my_item_loader.add_xpath(field_name='image_urls', xpath='//uc-pdp-media-carousel[@slot="media-content"]/*/img'
                                                                '/@src')
        return my_item_loader.load_item()
