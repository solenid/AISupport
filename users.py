import requests
from data import data as dat

def GetBase():

    # Выполнение запроса
    userGetResp = requests.get(dat.urlUSERSget, params=dat.paramsForUserGet)
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
