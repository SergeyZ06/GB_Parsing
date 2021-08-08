# 1. Написать программу, которая собирает входящие письма из своего или тестового почтового
# ящика, и сложить информацию о письмах в базу данных (от кого, дата отправки, тема письма,
# текст письма).

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from pymongo import MongoClient


# Класс для сбора информации о входящих письмах
class MailParser:
    def __init__(self, url_mail):
        self.url_mail = url_mail

        # Настойки браузера:
        # не спрашивать об уведомлениях
        preferences = {"profile.default_content_setting_values.notifications": 2}
        driver_chrome_options = ChromeOptions()
        driver_chrome_options.add_experimental_option(name='prefs', value=preferences)
        # driver_chrome_options.add_argument('--headless')

        # Подключение драйвера
        path_to_webdriver = fr'E:\MyDocuments\GeekBrains\6. Parsing\7th lesson\7th hometask\chromedriver.exe'
        self.driver_chrome = webdriver.Chrome(executable_path=path_to_webdriver, options=driver_chrome_options)

    # Метод для авторизации в почтовом сервисе
    def mail_login(self, mail_login, mail_password):
        self.driver_chrome.get(url=self.url_mail)

        # Заполнение формы логина
        element_input_email = self.driver_chrome.find_element_by_xpath(xpath=r'//input[@type="email"]')
        element_input_email.send_keys(mail_login)

        # Заполнение формы пароля
        element_input_password = self.driver_chrome.find_element_by_xpath(xpath=r'//input[@type="password"]')
        element_input_password.send_keys(mail_password)

        # Нажатие кнопки авторизации
        element_button_enter = self.driver_chrome.find_element_by_xpath(xpath=r'//*[@id="login-view"]/div[2]/div/div[1]'
                                                                              r'/form/div[4]/button')
        element_button_enter.click()

    # Метод для сбора информации о входящих письмах
    def mail_parse(self):
        # Лист для хранения информации о письмах
        list_mails = []

        # Отклонить всплывающее окно
        try:
            WebDriverWait(self.driver_chrome, 5).until(method=expected_conditions.alert_is_present())
            alert = self.driver_chrome.switch_to.alert
            alert.dismiss()
        except Exception as exc:
            print(exc)

        # Поиск всех элементов "письма" на странице
        elements_mails = self.driver_chrome.find_elements_by_xpath(xpath=r'//li[contains(@style, "list-item")]')

        # Переход по всем элементам "письма" на странице
        for element_mail in elements_mails:
            # Словарь для хранения информации о каждом письме
            dict_mail = {}

            # Открытие письма
            element_mail.click()

            # Ожидать пока не появится кнопка "Подбробно", затем нажать кнопку
            button_expand = WebDriverWait(self.driver_chrome, 5).\
                until(method=expected_conditions.
                      presence_of_element_located((By.XPATH, r'//button[@class="expander bg-transparent '
                                                             r'pt-s hover-ul limit-width"]')))
            button_expand.click()

            # Ожидать пока не появится информация об отправителе
            element_address = WebDriverWait(self.driver_chrome, 5).\
                until(method=expected_conditions.
                      presence_of_element_located((By.XPATH, r'//button[@class="mr-button secondary print"]')))
            dict_mail['from'] = element_address.text

            # Получение информации о дате отправления письма
            element_date = self.driver_chrome.find_element_by_xpath(
                xpath=r'//small[@class="date mt-xs content-fg selectable"]')
            dict_mail['date'] = element_date.text

            # Получении информации о теме письма
            element_subject = self.driver_chrome.find_element_by_xpath(
                xpath=r'//div[@class="subject text-break selectable"]')
            dict_mail['subject'] = element_subject.text

            # Получение информации о тексте письма
            element_text = self.driver_chrome.find_element_by_id(id_=r'mail-body')
            dict_mail['text'] = element_text.text

            # Добавление информации о письме в список
            list_mails.append(dict_mail.copy())

        #
        self.mails_to_mongo(list_mails=list_mails)
        self.driver_chrome.close()

    # Метод для записи информации о письмах в MongoDB
    @staticmethod
    def mails_to_mongo(list_mails):
        # Если список писем не пустой
        if len(list_mails) > 0:
            # Создать подключение к MongoDB
            mongo_db_name = r'GB_parsing'
            mongo_collection_name = r'selenium_mail'

            mongo_client = MongoClient(host='localhost', port=27017)
            mongo_db = mongo_client[mongo_db_name]

            # Если БД не обнаружена
            if mongo_db_name not in mongo_client.list_database_names():
                # создать БД и коллекцию в ней
                mongo_db.create_collection(mongo_collection_name)

            # Для каждого письма в списке писем
            for mail in list_mails:
                # записать в БД новую коллекцию с информацией о письме
                mongo_db[mongo_collection_name].insert_one({
                    'from': mail['from'],
                    'date': mail['date'],
                    'subject': mail['subject'],
                    'text': mail['text']
                })

            mongo_client.close()


# Переменные для хранения информации для подключения к почте
my_url_mail = r'https://mail.tutanota.com/login'
my_mail_login = r'gb_parsing@tutanota.com'
my_mail_password = r'kX5U7lJDYgM7Na69'

# Создание объекта и вызов методов для сбора информации о входящих письмах
my_MailParser = MailParser(url_mail=my_url_mail)
my_MailParser.mail_login(mail_login=my_mail_login, mail_password=my_mail_password)
my_MailParser.mail_parse()
