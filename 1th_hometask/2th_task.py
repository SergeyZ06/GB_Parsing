# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json

# Переменная для хранения ссылки на список репозиториев на GitHub для авторизованных пользователей
GitHub_url_repos = r'https://api.github.com/user/repos'
# Переменная для хранения Personal access token
GitHub_token = r'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'
# Headers для GET-запроса
headers = {fr'Authorization': fr'token {GitHub_token}'}
# Переменная для хранения имени файла для записи JSON объекта
file_json = r'2th_task.json'

# Попытка получить список репозиториев пользователя без аутентификации
req = requests.get(url=GitHub_url_repos)
print(f'Attempt to get repositories list without authentication:\n{req.text}\n')
# Ответ:
# {"message":"Requires authentication",
# "documentation_url":"https://docs.github.com/rest/reference/repos#list-repositories-for-the-authenticated-user"}

# Попытка получить список репозиториев пользователя с аутентификацией посредством личного токена доступа
req = requests.get(url=GitHub_url_repos, headers=headers)
print(f'Attempt to get repositories list with authentication via personal access token:\n(only first one hundred'
      f' characters are shown)\n{req.text[0:100]}\n')
# Ответ:
# [{"id":323058628,"node_id":"MDEwOlJlcG9zaXRvcnkzMjMwNTg2Mjg=","name":"Basics_of_Python","full_name":

# Переменная для хранения полученного JSON объекта
data_json = json.dumps(req.text)

# Сохранение JSON объекта в файл
with open(file=file_json, mode='w') as file:
    file.write(data_json)
