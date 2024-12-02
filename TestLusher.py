import requests
from vk_api import VkApiError
import GetInfoFromVK as getinfo
import GetToken as gt
from ColorCheck import colorCheck
# import users
import numpy as np
from tensorflow import keras

TOKEN = gt.getToken()

def getPostsPhoto(userID: str):
    resPhotos = [[],[]]
    vk = getinfo.getVKSession(TOKEN)
    if vk is None:
        exit()

    try:
        dataForWallGetById = vk.wall.get(owner_id=userID, count=10, filter='owner', extended=0, offset=0)
    except VkApiError as e:
        print(f"Ошибка при получении постов: {e}")
        return []

    for elements in dataForWallGetById['items']:
        for element in elements['attachments']:  # Указываем параметр, который нас интересует в посте
            if('photo' in element):
                print(element['photo'])
                photo = element['photo']['orig_photo']['url']
                photoId = element['photo']['id']
                resPhotos[0].append(photo)
                resPhotos[1].append(photoId)
    return resPhotos
# Функция для установки цвета текста с использованием ANSI escape codes
#def print_rgb(r, g, b, text):
    #print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")

def whatIsColorMean(indexLargeElement, countColor):
    if indexLargeElement == 0:
        countColor['blue']+=1

    if indexLargeElement == 1:
        countColor['yellow'] += 1

    if indexLargeElement == 2:
        countColor['green'] += 1

    if indexLargeElement == 3:
        countColor['red'] += 1


def testLusher(x, countColor):
    modelBlue = keras.models.load_model('AiModel/RGB+/my_model.keras')
    modelYellow = keras.models.load_model('AiModel/RGB+/my_modelYELLOW.keras')
    modelGreen = keras.models.load_model('AiModel/RGB+/my_modelGREEN.keras')
    modelRed = keras.models.load_model('AiModel/RGB+/my_modelRED.keras')

    predictionBlue = modelBlue.predict(x)
    predictionYellow = modelYellow.predict(x)
    predictionGreen = modelGreen.predict(x)
    predictionRed = modelRed.predict(x)

    sumPrediction = [sum(predictionBlue), sum(predictionYellow), sum(predictionGreen), sum(predictionRed)]
    indexLargeElement = sumPrediction.index(max(sumPrediction))
    whatIsColorMean(indexLargeElement, countColor)

    #print("Вывод для наглядного просмотра")

    #print("For Blue")
    InputDatasize = x.size
    counter = 0
    for i in predictionBlue:
        if (counter < InputDatasize):
            #print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
            counter += 1

    #print("For Yellow")
    InputDatasize = x.size
    counter = 0
    for i in predictionYellow:
        if (counter < InputDatasize):
            #print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
            counter += 1

    #print("For Green")
    InputDatasize = x.size
    counter = 0
    for i in predictionGreen:
        if (counter < InputDatasize):
            #print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
            counter += 1

    #print("For Red")
    InputDatasize = x.size
    counter = 0
    for i in predictionRed:
        if (counter < InputDatasize):
            #print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
            counter += 1


def startTestLusher(user_id: str):
    result = getPostsPhoto(user_id)
    if(result == []):
        return "Мы не смогли получить данные\nВозможно, пользователь, которого вы проверяете, не даёт доступ к данным."
    #print(result)

    countColor = {
        'blue': 0,
        'red': 0,
        'yellow': 0,
        "green": 0
    }
    for i in result[0]:
        #print("New url => " + i)
        testLusher(np.array(colorCheck(i, 20)), countColor)

    mostPopularColor = (max(countColor, key=countColor.get))

    message = "Не определён"

    if(mostPopularColor == 'yellow'):
        message = (" Самый часто используемый цвет на фото данного пользователя: ЖЕЛТЫЙ \n" +
                   "Это значит что человек попадает под желтый тип" +
                   "\nЖелтый тип - общительный, отзывчивый человек.  Им хорошо подходят  широкие социальные контакты.")
    if(mostPopularColor == 'blue'):
        message = (" Самый часто используемый цвет на фото данного пользователя: СИНИЙ \n" +
                   "Это значит что человек попадает под синий тип" +
                   "\nСиний тип - спокойный и уверенный в себе человек. Таким людям важно чувствовать себя в безопасности, быть всегда защищенными.")
    if (mostPopularColor == 'red'):
        message = (" Самый часто используемый цвет на фото данного пользователя: КРАСНЫЙ \n" +
                   "Это значит что человек попадает под красный тип" +
                   "\nКрасный тип - энергичный человек. Такие люди чувствует себя комфортно в активной деятельности.")
    if (mostPopularColor == 'green'):
        message = (" Самый часто используемый цвет на фото данного пользователя: ЗЕЛЁНЫЙ \n" +
                    "Это значит что человек попадает под зелёный тип" +
                    "\nЗеленый тип - настойчивый, но робкий человек. Ему комфортно в условиях, которые дают ощущение значимости и достоинства.")
    return message
