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
        # не спрашивать об уведомлениях,
        # запускать браузер в полноэкранном режиме
        preferences = {"profile.default_content_setting_values.notifications": 2}
        self.driver_chrome_options = ChromeOptions()
        self.driver_chrome_options.add_experimental_option(name='prefs', value=preferences)
        self.driver_chrome_options.add_argument("--start-maximized")
        # driver_chrome_options.add_argument('--headless')

        # Переменаая для хранения пути к драйверу
        self.path_to_webdriver = fr'E:\MyDocuments\GeekBrains\6. Parsing\7th lesson\7th hometask\chromedriver.exe'

    # Метод для сбора информации о товарах с mvideo.ru
    def get_mvideo_bestsellers(self):
        # Переменная для хранения адреса магазина
        url = r'https://www.mvideo.ru'
        # Список для сбора заголовков товаров
        list_titles = []
        # Список для сбора цен товаров
        list_prices = []
        # Список для хранения информации о товарах
        list_bestsellers = []

        # Подключение драйвера
        driver_chrome = webdriver.Chrome(executable_path=self.path_to_webdriver, options=self.driver_chrome_options)
        # Переход по по адресу магазина
        driver_chrome.get(url=url)

        # Путь к кнопке прокрутки товаров
        xpath_button_scroll = r'/html/body/div[2]/div/div[3]/div/div[4]/div/div[2]/div/div[1]/a[@class="next-btn' \
                              r' c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right"]'
        # Ожидать появления кнопки прокрутки товаров
        element_button_scroll = WebDriverWait(driver_chrome, 5).\
            until(expected_conditions.
                  presence_of_element_located((By.XPATH, xpath_button_scroll)))

        # Пока есть кнопка
        while element_button_scroll:
            # Проверить, чтокнопка всё ещё есть
            try:
                element_button_scroll = WebDriverWait(driver_chrome, 5).\
                    until(expected_conditions.
                          presence_of_element_located((By.XPATH, xpath_button_scroll)))
            except TimeoutException:
                element_button_scroll = None

            # Получить все элементы, в которых хранится информация о товарах
            elements_bestsellers = WebDriverWait(driver_chrome, 5). \
                until(expected_conditions.
                      presence_of_all_elements_located((By.XPATH, r'//ul[contains(@data-init-param, '
                                                                  r'"Хиты продаж")]/li')))

            # Для всех полученных элементов
            for element_bestseller in elements_bestsellers:
                # Найти найменование товара
                title = element_bestseller. \
                    find_element_by_xpath(xpath=r'.//a[@class="fl-product-tile-title__link'
                                                r' sel-product-tile-title"]').text
                # Найти стоимость товара
                price = element_bestseller.find_element_by_xpath(xpath=r'.//span[@itemprop="price"]').text

                # Если данный товар отсутствует в списке собранных товаров,
                # то добавить в списки информацию о товаре
                if title not in list_titles and title != '':
                    list_titles.append(title)
                    list_prices.append(price)
            # Если кнопка всё ещё есть, то нажать её
            if element_button_scroll:
                element_button_scroll.click()

        driver_chrome.close()

        # Для каждого товара в списке товаров
        for i in range(len(list_titles)):
            # добавить информацию о товаре в словарь
            dict_bestseller = {}
            dict_bestseller['title'] = list_titles[i]
            dict_bestseller['price'] = int(list_prices[i].replace('₽', '').strip().replace(' ', ''))
            dict_bestseller['source'] = url
            # добавить словарь в список для хранения информации о товарах
            list_bestsellers.append(dict_bestseller.copy())

        # Вызвать метод для записи информации о товарах в MongoDB
        self.bestsellers_to_mongo(list_bestsellers=list_bestsellers)

    # Метод для сбора информации о товарах с onlinetrade.ru
    # Принцип работы данного метода аналогичен вышеописанному методу,
    # за исключением других xpath к элементам сайта магазина
    def get_onlinetrade_bestsellers(self):
        url = r'https://www.onlinetrade.ru/'
        list_titles = []
        list_prices = []
        list_bestsellers = []

        driver_chrome = webdriver.Chrome(executable_path=self.path_to_webdriver, options=self.driver_chrome_options)
        driver_chrome.get(url=url)

        xpath_button_scroll = r'//*[@id="tabs_hits"]/div[1]/span[2][@aria-disabled="false"]'
        element_button_scroll = WebDriverWait(driver_chrome, 5).\
            until(expected_conditions.presence_of_element_located((By.XPATH, xpath_button_scroll)))

        while element_button_scroll:
            try:
                element_button_scroll = WebDriverWait(driver_chrome, 5).\
                    until(expected_conditions.
                          presence_of_element_located((By.XPATH, xpath_button_scroll)))
            except TimeoutException:
                element_button_scroll = None

            elements_bestsellers = WebDriverWait(driver_chrome, 5). \
                until(expected_conditions.
                      presence_of_all_elements_located((By.XPATH, r'//*[@id="tabs_hits"]/div[2]/div/div/div')))

            for element_bestseller in elements_bestsellers:
                title = element_bestseller.find_element_by_xpath(xpath=r'.//a[@class="indexGoods__item__name"]').text
                price = element_bestseller.find_element_by_xpath(xpath=r'.//span[contains(@class, "price")]').text

                if title not in list_titles and title != '':
                    list_titles.append(title)
                    list_prices.append(price)

            if element_button_scroll:
                element_button_scroll.click()

        driver_chrome.close()

        for i in range(len(list_titles)):
            dict_bestseller = {}
            dict_bestseller['title'] = list_titles[i]
            dict_bestseller['price'] = int(list_prices[i].replace('₽', '').strip().replace(' ', ''))
            dict_bestseller['source'] = url
            list_bestsellers.append(dict_bestseller.copy())

        self.bestsellers_to_mongo(list_bestsellers=list_bestsellers)

    # Метод для записи информации о товарах в MongoDB
    @staticmethod
    def bestsellers_to_mongo(list_bestsellers):
        # Если список товаров не пустой
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

            # Для каждого товара в списке товаров
            for bestseller in list_bestsellers:
                # записать в БД новую коллекцию с информацией о товаре
                mongo_db[mongo_collection_name].insert_one({
                    'title': bestseller['title'],
                    'price': bestseller['price'],
                    'source': bestseller['source']
                })

            mongo_client.close()


my_bestsellers = BestSellers()
my_bestsellers.get_mvideo_bestsellers()
my_bestsellers.get_onlinetrade_bestsellers()
