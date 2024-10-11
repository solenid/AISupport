# c5aebac8c5aebac8c5aebac8fac68ec9b3cc5aec5aebac8a2a6aaffbc053a29d4c6cf6d
# https://<адрес-сервера>/method/<имя-API-метода>?<параметры>
# <адрес-сервера> — один из адресов API ВКонтакте:
# • api.vk.com
# • api.vk.ru
# •<имя-API-метода> — имя раздела и API-операции для вызова, например users.get или likes.add.
# •<параметры> — параметры, которые передаются методу в строке запроса, например ...?v=5.199&p1=v1.
#
# https://api.vk.ru/method/account.getInfo?fields
# account.getInfo
# answer2 = requests.get("https://api.vk.ru/method/users.get?user_ids=aidkhall&access_token=c5aebac8c5aebac8c5aebac8fac68ec9b3cc5aec5aebac8a2a6aaffbc053a29d4c6cf6d&v=5.131")
# https://vk.com/sveeecha
# https://vk.com/aidkhall
# https://vk.com/wall394305035_1304
# c5aebac8c5aebac8c5aebac8fac68ec9b3cc5aec5aebac8a2a6aaffbc053a29d4c6cf6d



# START

import requests
from enum import Enum

# Замените 'YOUR_ACCESS_TOKEN' на ваш токен доступа
ACCESS_TOKEN = 'c5aebac8c5aebac8c5aebac8fac68ec9b3cc5aec5aebac8a2a6aaffbc053a29d4c6cf6d'
USER_ID = 'aidkhall'  # Замените на ID пользователя
POST_ID = 'vk_post_394305035_1304'   # Замените на ID поста !!! используется в getById
COUNT_POSTS = 10 # количество постов
FILTER = 'owner' # Записи владельца или других пользователей
OFFSET = 0 # Сдвиг
class CHOICE(Enum):
    TEXT = 'text'
    PHOTO = 'photo'

YOURCHOICE = CHOICE.TEXT.value
print(YOURCHOICE)



# URL для запроса к API (МЕТОД WALL.GETBYID)
url = 'https://api.vk.com/method/wall.getById'

# URL для запроса к API (МЕТОД WALL.GETBYID)
url2 = 'https://api.vk.com/method/wall.get'

# Параметры запроса
params = {
    'access_token': ACCESS_TOKEN,
    'owner_id': f'{USER_ID}',
    'offset': f'{OFFSET}',
    'count': f'{COUNT_POSTS}',
    'filter': f'{FILTER}',
    'v': '5.131'  # Версия API
}

# Выполнение запроса
response = requests.get(url2, params=params)
data = response.json()
# print(data)
print(data['response']['items'])



if(YOURCHOICE == "text"):
    print(f"Проверка на {YOURCHOICE}")
    for elements in data['response']['items']:
        if (elements['text'] != ""):
            print("--------------------------------------")
            print(f"id => {elements['id']}")
            print(elements['text'])
            print("--------------------------------------\n")
        else:
            print("--------------------------------------")
            print(f"id => {elements['id']}")
            print("Текста нет")
            print("--------------------------------------\n")

if(YOURCHOICE == "photo"):
    print(f"Проверка на {YOURCHOICE}")
    for elements in data['response']['items']:
        for element in elements['attachments']:  # Указываем параметр, который нас интересует в посте
            photo = element['photo']['orig_photo']
            print(photo)
            if (photo['url'] != ""):
                print("--------------------------------------")
                print(f"id => {elements['id']}")
                print(f"Size original photo: {photo['width']}x{photo['height']}")
                print(f"Type => {element['type']}")
                print(f"Photo url => {photo['url']}")
                print("--------------------------------------\n")

            else:
                print("--------------------------------------")
                print(f"id => {elements['id']}")
                print("фото нет")
                print("--------------------------------------\n")