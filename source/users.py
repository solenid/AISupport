import requests
from enum import Enum

def GetBase(USER_ID):
    # Замените 'YOUR_ACCESS_TOKEN' на ваш токен доступа
    ACCESS_TOKEN = 'c5aebac8c5aebac8c5aebac8fac68ec9b3cc5aec5aebac8a2a6aaffbc053a29d4c6cf6d'
    #USER_ID = 'aidkhall'  # Замените на ID пользователя

    urlUSERSget = 'https://api.vk.com/method/users.get'
    # Параметры запроса
    paramsForUserGet = {
        'access_token': ACCESS_TOKEN,
        'user_ids': f'{USER_ID}',
        'fields': ' status , photo, bdate, universities, interests, schools',
        'v': '5.131'  # Версия API
    }

    # Выполнение запроса
    userGetResp = requests.get(urlUSERSget, params=paramsForUserGet)
    data = userGetResp.json()
    #print(data)
    # Если ответ получен
    if ('response' in data):
        # Если ответ не пуст
        if (len(data['response']) != 0):

            print('Имя: ' + data['response'][0]['first_name'] + ' ' + data['response'][0]['last_name'])
            print('Статус: ' + data['response'][0]['status'])
            print('Ссылка на фото профиля: ' + data['response'][0]['photo'])

            # Школы
            if ('schools' in data['response'][0]):
                for school in data['response'][0]['schools']:
                    print(school['name'])

            # Если указан университет
            if ('universities' in data['response'][0]):
                print('Университет: ' + data['response'][0]['universities'][0]['name'] + ' - ' +
                      data['response'][0]['universities'][0]['faculty_name'] + ' - ' +
                      data['response'][0]['universities'][0]['chair_name'])
        else:
            print(data)
    else:
        print(data)
