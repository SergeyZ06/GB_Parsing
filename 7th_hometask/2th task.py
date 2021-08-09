# 2. Написать программу, которая собирает «Хиты продаж» с сайтов техники М.видео, ОНЛАЙН
# ТРЕЙД и складывает данные в БД. Магазины можно выбрать свои. Главный критерий выбора:
# динамически загружаемые товары.

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pymongo import MongoClient


class BestSellers:
    def __init__(self):
        # Настойки браузера:
        # не спрашивать об уведомлениях
        preferences = {"profile.default_content_setting_values.notifications": 2}
        driver_chrome_options = ChromeOptions()
        driver_chrome_options.add_experimental_option(name='prefs', value=preferences)
        driver_chrome_options.add_argument("--start-maximized")
        # driver_chrome_options.add_argument('--headless')

        # Подключение драйвера
        path_to_webdriver = fr'E:\MyDocuments\GeekBrains\6. Parsing\7th lesson\7th hometask\chromedriver.exe'
        self.driver_chrome = webdriver.Chrome(executable_path=path_to_webdriver, options=driver_chrome_options)

    def get_mvideo_bestsellers(self):
        url = r'https://www.mvideo.ru'
        list_titles = []
        list_prices = []
        list_bestsellers = []

        self.driver_chrome.get(url=url)

        xpath_button_scroll = r'/html/body/div[2]/div/div[3]/div/div[4]/div/div[2]/div/div[1]/a[@class="next-btn' \
                              r' c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right"]'
        element_button_scroll = WebDriverWait(self.driver_chrome, 5).\
            until(expected_conditions.
                  presence_of_element_located((By.XPATH, xpath_button_scroll)))

        while element_button_scroll:
            elements_bestsellers = WebDriverWait(self.driver_chrome, 5). \
                until(expected_conditions.
                      presence_of_all_elements_located((By.XPATH, r'//ul[contains(@data-init-param, '
                                                                  r'"Хиты продаж")]/li')))

            for element_bestseller in elements_bestsellers:
                title = element_bestseller. \
                    find_element_by_xpath(xpath=r'.//a[@class="fl-product-tile-title__link'
                                                r' sel-product-tile-title"]').text

                price = element_bestseller.find_element_by_xpath(xpath=r'.//span[@itemprop="price"]').text

                if title not in list_titles and title != '':
                    list_titles.append(title)
                    list_prices.append(price)

            element_button_scroll.click()
            try:
                element_button_scroll = WebDriverWait(self.driver_chrome, 5).\
                    until(expected_conditions.
                          presence_of_element_located((By.XPATH, xpath_button_scroll)))
            except TimeoutException:
                element_button_scroll = None

        self.driver_chrome.close()

        for i in range(len(list_titles)):
            dict_bestseller = {}
            dict_bestseller['title'] = list_titles[i]
            dict_bestseller['price'] = int(list_prices[i].replace('₽', '').strip().replace(' ', ''))
            dict_bestseller['source'] = url
            list_bestsellers.append(dict_bestseller.copy())

        self.bestsellers_to_mongo(list_bestsellers=list_bestsellers)

    def get_onlinetrade_bestsellers(self):
        # url = r'https://www.onlinetrade.ru/'
        pass

    # Метод для записи информации о письмах в MongoDB
    @staticmethod
    def bestsellers_to_mongo(list_bestsellers):
        # Если список писем не пустой
        if len(list_bestsellers) > 0:
            # Создать подключение к MongoDB
            mongo_db_name = r'GB_parsing'
            mongo_collection_name = r'selenium_bestsellers'

            mongo_client = MongoClient(host='localhost', port=27017)
            mongo_db = mongo_client[mongo_db_name]

            # Если БД не обнаружена
            if mongo_db_name not in mongo_client.list_database_names():
                # создать БД и коллекцию в ней
                mongo_db.create_collection(mongo_collection_name)

            # Для каждого письма в списке писем
            for bestseller in list_bestsellers:
                # записать в БД новую коллекцию с информацией о письме
                mongo_db[mongo_collection_name].insert_one({
                    'title': bestseller['title'],
                    'price': bestseller['price'],
                    'source': bestseller['source']
                })

            mongo_client.close()


my_bestsellers = BestSellers()
my_bestsellers.get_mvideo_bestsellers()
