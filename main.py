# https://vk.com/sveeecha
# https://vk.com/aidkhall
# c5aebac8c5aebac8c5aebac8fac68ec9b3cc5aec5aebac8a2a6aaffbc053a29d4c6cf6d
# f5047191f5047191f5047191caf624eadeff504f5047191920feda5943381a1caa2ddf2

# START
import requests
from source import data
import users


def userIdInteger():
    responseForUtilsResolveScreenName = requests.get(data.urlUtilsResolveScreenName,
                                                     params=data.paramsForUtilsResolveScreenName)
    dataForUtilsResolveScreenName = responseForUtilsResolveScreenName.json()
    print(dataForUtilsResolveScreenName)
    data.USER_ID_INTEGER = dataForUtilsResolveScreenName['response']['object_id']
    print(data.USER_ID_INTEGER)
    data.paramsForFriendsGet['user_id'] = data.USER_ID_INTEGER # переопределение USER_ID_INTEGER

def userGetCountFriends():
    responseForFriendsGet = requests.get(data.urlFriendsGet, params=data.paramsForFriendsGet)
    dataForFriendsGet = responseForFriendsGet.json()
    print(dataForFriendsGet)
    data.COUNT_FRIEND = dataForFriendsGet['response']['count']
    print(data.COUNT_FRIEND)

# Выполнение запроса GetById
def userGetInfo(choice):
    responseForWallGetById = requests.get(data.urlWallGetById, params=data.paramsForWallGetById)
    dataForWallGetById = responseForWallGetById.json()
    # print(data)
    # print(dataForWallGetById['response']['items'])
    if (choice == "text"):
        print(f"Проверка на {choice}")
        for elements in dataForWallGetById['response']['items']:
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

    if (choice == "photo"):
        print(f"Проверка на {choice}")
        for elements in dataForWallGetById['response']['items']:
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




def main():
    print("start main")
    YOURCHOICE = data.CHOICE.TEXT.value
    print("Вы выбрали: " + YOURCHOICE)

    userGetInfo(YOURCHOICE)
    
    #Вызов новой функции
    users.GetBase()

    print("end main")

main()