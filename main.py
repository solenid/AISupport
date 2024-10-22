# START
import requests
from data import data
from colorCHECK import colorCHECK
import UsersGet
import numpy as np
from tensorflow import keras

# Функция для установки цвета текста с использованием ANSI escape codes
def print_rgb(r, g, b, text):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")

def whatIsColorMean(indexLargeElement):
    if(indexLargeElement == 0):
        print("Синий и его оттенки доминируют")
        print("Это означает, что:\n"
              "Синий тип - спокойный и уверенный в себе человек. Таким людям важно чувствовать себя в безопасности, быть всегда защищенными.")

    if (indexLargeElement == 1):
        print("Yellow is dominated")
        print("Это означает, что:\n"
              "Желтый тип - общительный, отзывчивый человек.  Им хорошо подходят  широкие социальные контакты.")


    if (indexLargeElement == 2):
        print("Green is dominated")
        print("Это означает, что:\n"
              "Зеленый тип - настойчивый, но робкий человек. Ему комфортно в условиях, которые дают ощущение значимости и достоинства.")


    if (indexLargeElement == 3):
        print("Red is dominated")
        print("Это означает, что:\n"
              "Красный тип - энергичный человек. Такие люди чувствует себя комфортно в активной деятельности.")



def testLusher(x):
    modelBlue = keras.models.load_model('AiModel/my_model.keras')
    modelYellow = keras.models.load_model('AiModel/my_modelYELLOW.keras')
    modelGreen = keras.models.load_model('AiModel/my_modelGREEN.keras')
    modelRed = keras.models.load_model('AiModel/my_modelRED.keras')
    # model.summary()

    predictionBlue = modelBlue.predict(x)
    predictionYellow = modelYellow.predict(x)
    predictionGreen = modelGreen.predict(x)
    predictionRed = modelRed.predict(x)

    sumPrediction = [sum(predictionBlue), sum(predictionYellow),sum(predictionGreen), sum(predictionRed) ]
    indexLargeElement = sumPrediction.index(max(sumPrediction))
    whatIsColorMean(indexLargeElement)

    print("Вывод для наглядного просмотра")

    print("For Blue")
    InputDatasize = x.size
    counter = 0
    for i in predictionBlue:
        if (counter < InputDatasize):
            print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
            counter += 1

    print("For Yellow")
    InputDatasize = x.size
    counter = 0
    for i in predictionYellow:
        if (counter < InputDatasize):
            print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
            counter += 1

    print("For Green")
    InputDatasize = x.size
    counter = 0
    for i in predictionGreen:
        if (counter < InputDatasize):
            print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
            counter += 1

    print("For Red")
    InputDatasize = x.size
    counter = 0
    for i in predictionRed:
        if (counter < InputDatasize):
            print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
            counter += 1


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

    arrayUrl = ["https://sun9-37.userapi.com/impg/lFe4xJ_TqrTPMpgoHXvhljxd2NBnarla9zw70Q/AhhMFDgYBO8.jpg?size=1080x1075"
                "&quality=96&sign=988c89dd24b6e2bc1ba0f5155909835d&type=album",
                "https://sun9-2.userapi.com/impg/yf49RCWpoxmuUnJOoq-8O-bXZioOCRIilNexcA/P8yZRI9V8Fg.jpg?size=1181x1772"
                "&quality=95&sign=f84cc1d13b90cee3996d297471823974&type=album",
                "https://sun9-13.userapi.com/impg/hHiPuY8A2bH61gPdHAVav7Fn8aLaKvji6t5u9g/M9BMxtJ1zp8.jpg?size=2400x1600"
                "&quality=95&sign=e6e3209d032d2c36313a2dc1394cd242&type=album",
                "https://sun9-57.userapi.com/impg/E3Loj8E7sIpybdC8Bhtaa_rsF9nDjgpcqpNhlw/4lwKFEX-OlA.jpg?size=880x1080"
                "&quality=96&sign=45ea0b9d3204888ee409828f3704bb11&type=album",
                "https://sun9-71.userapi.com/impf/c622924/v622924905/4afeb/d2Fr-v9bViA.jpg?size=238x293&quality=96"
                "&sign=d0608d223f64ba4d6b10a6dd094228ec&type=album"]

    for i in arrayUrl:
        print("New url => " + i)
        testLusher(np.array(colorCHECK(i,15)))

    print("end main")

main()