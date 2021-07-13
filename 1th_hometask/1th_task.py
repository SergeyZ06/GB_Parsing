# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

# Переменная для хранения ника на GitHub
GitHub_username = r'SergeyZ06'
# Переменная для хранения ссылки на список репозиториев на GitHub
GitHub_url_repos = fr'https://api.github.com/users/{GitHub_username}/repos'
# Headers для GET-запроса
headers = {'Username': fr'{GitHub_username}'}
# Переменная для хранения имени файла для записи JSON объекта
file_json = r'1th_task.json'

# Инициализация GET-запроса к GitHub
req = requests.get(url=GitHub_url_repos, headers=headers)
# Переменная для хранения полученного JSON объекта
data_json = json.dumps(req.text)

# Сохранение JSON объекта в файл
with open(file=file_json, mode='w') as file:
    file.write(data_json)
