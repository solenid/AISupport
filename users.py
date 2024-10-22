import requests

SERVICE_TOKEN = 'c0754f89c0754f89c0754f892cc3543dbccc075c0754f89a763ae63b86c6df9fd886d21'
urlUSERSget = 'https://api.vk.com/method/users.get'

def GetBase(USER_ID):
    paramsForUserGet = {
        'access_token': SERVICE_TOKEN,
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
