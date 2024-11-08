import vk_api
import time
import tkinter as tk
from CheckSpelling import *
from WordsFinder import *
from GetPosts import *
from GetToken import *
from DataBaseInterface import *

TOKEN = getToken()
dataDB = []

def getVKSession(token):
    try:
        vkSession = vk_api.VkApi(token=token)
        vk = vkSession.get_api()
        return vk
    except VkApiError as e:
        print(f"Ошибка при подключении к VK API: {e}")
        return None


def getNumberOfFriends(vk, userID):
    try:
        response = vk.friends.get(user_id=userID, count=0)
        return response['count']
    except VkApiError as e:
        print(f"Ошибка при получении друзей: {e}")
        return None

def getTotalComments(posts):
    return sum(post.get('comments', {}).get('count', 0) for post in posts)

def getTotalLikes(posts):
    return sum(post.get('likes', {}).get('count', 0) for post in posts)

def getPostsText(posts):
    return [post.get('text', '') for post in posts]

def getPublicsTheme(vk, userID):
    try:
        response = vk.groups.get(user_id=userID, count=0)
        return response['count']
    except VkApiError as e:
        print(f"Ошибка при получении групп: {e}")
        return None

def getCriteriaGrade(score):
    result = "Низкая"
    if score > 2:
        if score > 4:
            result = "Высокая"
        else:
            result = "Средняя"
    elif score < 0:
        result = "Не определено" #\n(веротяно нет постов или слов в них)"
    return result

def getGroupsTheme(vk, userID):
    dictionaryThemes = {}
    garbageThemesKeyWords = ["заблокирован", "закрытое", "закрытый", "недоступный", "недоступно"] # Здесь добавляем
                                                                        # ключевые слова ненужных нам тем (строчными)
    offset = 0
    count = 1000
    while True:
        try:
            response = vk.groups.get(
                user_id=userID,
                extended=1,
                fields='activity',
                offset=offset,
                count=count
            )
        except VkApiError as error:
            print(f"Ошибка при получении групп: {error}")
            break
        groups = response.get('items', [])
        if not groups:
            break
        for group in groups:
            activity = group.get('activity')
            if activity and not any(keyword in activity.lower() for keyword in garbageThemesKeyWords):
                if activity in dictionaryThemes:
                    dictionaryThemes[f'{activity}'] += 1
                else:
                    dictionaryThemes[f'{activity}'] = 1
        offset += count
    sortedDict = {key: value for key,
    value in sorted(dictionaryThemes.items(),
                    key=lambda item: item[1], reverse=True)}
    return list(sortedDict.keys())

def GetBase(vk, USER_ID):
    result = []
    fields = 'status, bdate, universities, interests, schools'
    try:
        response = vk.users.get(user_ids=USER_ID, fields=fields)
        # Если ответ получен и Если ответ не пуст
        if (len(response) != 0):
            result.append(f"Имя: {response[0]['first_name']}")
            dataDB.append(response[0]['first_name'])
            result.append(f"Фамилия: {response[0]['last_name']}")
            dataDB.append(response[0]['last_name'])
            #Дата рождения
            if ('bdate' in response[0]):
                result.append(f"Дата рождения: {response[0]['bdate']}")
                dataDB.append(response[0]['bdate'])
            #Статус
            if (len(response[0]['status']) != 0):
                result.append(f"Статус: {response[0]['status']}")
            # Школы
            if ('schools' in response[0]):
                result.append(f"Школы:")
                for school in response[0]['schools']:
                    result.append(f"- {school['name']}")
            # Если указан университет
            if ('universities' in response[0]):
                if (len(response[0]['universities']) != 0):
                    result.append(f"Университет: {response[0]['universities'][0]['name']} \n")
                    if 'faculty_name' in response[0]['universities']:
                        if 'chair_name' in response[0]['universities']:
                            result.append(f"{response[0]['universities'][0]['faculty_name']} - {response[0]['universities'][0]['chair_name']}")
                        else:
                            result.append(f"{response[0]['universities'][0]['faculty_name']}")
        else:
            print(response)
    except VkApiError as e:
        print(f"Ошибка при информации профиля: {e}")
    return result


def getInfoFromVK(userID: str, serviceToken, userToken):

    # Флаги оценок
    criteriaCommun = 0 # Общительность
    criteriaLiter = 0 # Грамотность
    criteriaConcen = 0 # Концентрация
    criteriaActivity = 0 # Активность
    criteriaRedFlag = 0 # Ред флаги
    result = [["ОБЩАЯ ИНФОРМАЦИЯ: ",f"Используемый user_id: {userID}"], ["RED FLAGs: "],["GREEN FLAGs: "],["Рекомендации:"]] # 0 - общая | 1 - red flags | 2 - green flags
    startTime = time.time()
    vk = getVKSession(serviceToken)
    if vk is None:
        exit()

    base = GetBase(vk, userID)
    for res in base:
        result[0].append(res)
    # 1. Количество друзей
    friendsNum = getNumberOfFriends(vk, userID)
    if friendsNum is not None:
        result[0].append(f"Количество друзей пользователя: {friendsNum}")
        dataDB.append(friendsNum)
        #Оценка общительности
        if friendsNum > 100:
            if friendsNum > 200:
                criteriaCommun += 2
            else:
                criteriaCommun += 1
    else:
        dataDB.append(friendsNum)


    # 2. Получение кол-ва постов за год
    posts = getPostsForLastYear(vk, userID)
    numPosts = len(posts)
    result.append(f"Всего постов за год: {numPosts}")
    dataDB.append(numPosts)
    if numPosts > 0:

        # Оценка Активности
        if numPosts > 2:
            if numPosts > 6:
                criteriaActivity = 6
            else:
                criteriaActivity = 4

        # 3. Общее количество комментариев за год
        totalComments = getTotalComments(posts)
        result[0].append(f"Общее количество комментариев за год: {totalComments}")
        dataDB.append(totalComments)
        # Оценка общительности
        if totalComments > (friendsNum*(0.2)):
            if totalComments > (friendsNum*(0.5)):
                criteriaCommun += 2
            else:
                criteriaCommun += 1

        # 4. Общее количество лайков за год
        totalLikes = getTotalLikes(posts)
        result[0].append(f"Общее количество лайков за год: {totalLikes}")
        dataDB.append(totalLikes)

        # Оценка общительности
        if totalLikes > (friendsNum*(0.50)):
            if totalLikes > (friendsNum*(0.75)):
                criteriaCommun += 2
            else:
                criteriaCommun += 1

        #!Если есть текст в постах
        postsText = getPostsText(posts)
        if postsText:
            # 5. Тексты постов за год и проверка на ошибки
            errCount = 0
            totalWords = 0
            for idx, text in enumerate(postsText, 1):
                totalWords += len(text.split())
                errors = checkSpelling(text)
                if errors:
                    errCount += len(errors)
            #!Если есть текст в постах СНОВА????????
            if (totalWords) > 0:
                result[1].append(f"Общее кол-во постов за год, содержащие грамматические ошибки : {errCount}")
                dataDB.append(errCount)
                #Оценка грамотности (точности)
                if (errCount) != 0:
                    if errCount/totalWords < 0.1:
                        criteriaLiter = 4
                else:
                    criteriaLiter = 6


                totalForbiddenCount = 0 # 6. Количество матерных постов
                totalGFWordCount = 0 # 6+ Количество постов по теме PR менеджемента
                searcRes = WordsSearch(postsText, totalGFWordCount, totalForbiddenCount)
                totalForbiddenCount = searcRes[0]
                totalGFWordCount = searcRes[1]
                result[1].append(f"Общее кол-во матерных постов: {totalForbiddenCount}")
                result[2].append(f"Общее кол-во релевантных постов: {totalGFWordCount}")

                dataDB.append(totalForbiddenCount) #Маты в базе данных

                # Оценка дивиации
                if totalForbiddenCount / numPosts > 0.15:
                    if totalForbiddenCount / numPosts > 0.25:
                        criteriaRedFlag += 2
                    else:
                        criteriaRedFlag += 1

                # Оценка сосредоточенности
                if totalGFWordCount > 0:
                    if totalGFWordCount / numPosts > 0.05:
                        criteriaConcen += 5
                    else:
                        criteriaConcen += 3

                # 7. Количество экстремистких слов в постах
                totalForbiddenCount = 0
                for text in postsText:
                    forbiddenCount = countExtremismWords(text)
                    totalForbiddenCount += forbiddenCount
                result[1].append(f"Общее кол-во экстремистских слов в постах: {totalForbiddenCount}")
                dataDB.append(totalForbiddenCount)

                # Оценка дивиации
                if totalForbiddenCount / totalWords > 0.05:
                    if totalForbiddenCount / totalWords > 0.15:
                        criteriaRedFlag += 2
                    else:
                        criteriaRedFlag += 1

                # 8. Количество слов-угроз в постах
                totalForbiddenCount = 0
                for text in postsText:
                    forbiddenCount = countThreatWords(text)
                    totalForbiddenCount += forbiddenCount
                result[1].append(f"Общее кол-во слов-угроз в постах: {totalForbiddenCount}")
                dataDB.append(totalForbiddenCount)
                # Оценка дивиации
                if totalForbiddenCount / totalWords > 0.05:
                    if totalForbiddenCount / totalWords > 0.15:
                        criteriaRedFlag += 2
                    else:
                        criteriaRedFlag += 1
            else:
                dataDB.append(0)
                dataDB.append(0)
                dataDB.append(0)
                dataDB.append(0)
                # Если слов все-таки нет
                result[0].append(f"Отсутствуют текстовые посты")
                criteriaConcen = -1
                criteriaRedFlag = -1
                criteriaLiter = -1
        else:
            dataDB.append(0)
            dataDB.append(0)
            dataDB.append(0)
            dataDB.append(0)
            result[0].append(f"Отсутствуют текстовые посты")
            criteriaConcen = -1
            criteriaRedFlag = -1
            criteriaLiter = -1
    else:
        dataDB.append(0)
        dataDB.append(0)
        dataDB.append(0)
        dataDB.append(0)
        dataDB.append(0)
        dataDB.append(0)

        result[0].append(f"Отсутствуют посты")
        criteriaConcen = -1
        criteriaRedFlag = -1
        criteriaLiter = -1
    # 9. Тематики групп пользователя
    vk = getVKSession(userToken)
    themes = getGroupsTheme(vk, userID)[:5] #Топ 5 тематик пользователя

    totalGFWordTheme = 0  # Количество тематик по теме PR менеджемента
    searcRes = WordsSearch(themes, totalGFWordTheme, 0)
    totalGFWordTheme = searcRes[1]
    #Оценка концентрации
    if totalGFWordTheme > 0:
        criteriaConcen += 2

    result[0].append("Топ 5 тематик групп пользователя:")
    for theme in themes:
        result[0].append(f"- {theme}")
    dataDB.append(themes[0])
    dataDB.append(55)
    dataDB.append('https://vk.com/h0w_to_survive')

    addUser(dataDB[0],dataDB[1],dataDB[2],dataDB[3],dataDB[4],
            dataDB[5],dataDB[6],dataDB[7],dataDB[8],dataDB[9],
            dataDB[10],dataDB[11],dataDB[12], dataDB[13])
    dataDB.clear()
    #10 ОЦЕНКА пользователя
    result[2].append(f"Общительность: {getCriteriaGrade(criteriaCommun)}")
    result[2].append(f"Грамотность: {getCriteriaGrade(criteriaLiter)}")
    result[2].append(f"Активность: {getCriteriaGrade(criteriaActivity)}")
    result[2].append(f"Вовлеченность: {getCriteriaGrade(criteriaConcen)}")
    result[1].append(f"Степень дивиации: {getCriteriaGrade(criteriaRedFlag)}")

    if criteriaRedFlag <= 2:
        if criteriaCommun > 4 and criteriaLiter > 4 and criteriaActivity > 4 and criteriaConcen > 4:
            result[3].append(f"ВЫСОКО РЕКОМЕНДУЮ на основании:\n Общительность,Грамотность,Активность,Вовлеченность - на высшем уровне")
        elif (criteriaCommun > 4 and criteriaLiter > 4):
            result[3].append(f"РЕКОМЕНДУЮ на основании:\n Общительность,Грамотность - на высшем уровне")
        elif (criteriaCommun > 4 and criteriaConcen > 4):
            result[3].append(f"РЕКОМЕНДУЮ на основании:\n Общительность,Вовлеченность - на высшем уровне")
        elif (criteriaCommun > 4 and criteriaActivity > 4):
            result[3].append(f"РЕКОМЕНДУЮ на основании:\n Общительность,Активность - на высшем уровне")
        elif (criteriaActivity > 4 and criteriaConcen > 4):
            result[3].append(f"РЕКОМЕНДУЮ на основании:\n Активность,Вовлеченность - на высшем уровне")
        elif (criteriaActivity > 4 and criteriaLiter > 4):
            result[3].append(f"РЕКОМЕНДУЮ на основании:\n Активность,Грамотность - на высшем уровне")
        elif (criteriaConcen > 4 and criteriaLiter > 4):
            result[3].append(f"РЕКОМЕНДУЮ на основании:\n Вовлеченность,Грамотность - на высшем уровне")
        elif (criteriaCommun > 4 or criteriaActivity > 4 or criteriaConcen > 4):
            if criteriaCommun > 4:
                result[3].append(f"Стоит обратить внимание так как Общительность - на высшем уровне")
            if criteriaActivity > 4:
                result[3].append(f"Стоит обратить внимание так как Активность - на высшем уровне")
            if criteriaConcen > 4:
                result[3].append(f"Стоит обратить внимание так как Вовлеченность - на высшем уровне")
        elif criteriaCommun > 2 and criteriaLiter > 2 and criteriaActivity > 2 and criteriaConcen > 2:
            result[3].append("Кандидат обладает средниими показателями, ему есть куда расти")
        else:
            result[3].append("НЕ РЕКОМЕНДУЮ на основании отсутвия необходимых качеств (Они на среднем-низком уровне)")
    else:
        if criteriaCommun > 4 and criteriaLiter > 4 and criteriaActivity > 4 and criteriaConcen > 4:
            result[3].append(f"РЕКОМЕНДУЮ на основании:\n Общительность,Грамотность,Активность,Вовлеченность - на высшем уровне\n !Следует обратить внимание на высокую степень дивиации!")
        elif (criteriaCommun > 4 and criteriaLiter > 4):
            result[3].append(f"Стоит обратить внимание так как Общительность,Грамотность - на высшем уровне\n !ВНИМАНИЕ высокая степень дивиации!")
        elif (criteriaCommun > 4 and criteriaConcen > 4):
            result[3].append(f"Стоит обратить внимание так как Общительность,Вовлеченность - на высшем уровне\n !ВНИМАНИЕ высокая степень дивиации!")
        elif (criteriaCommun > 4 and criteriaActivity > 4):
            result[3].append(f"Стоит обратить внимание так как Общительность,Активность - на высшем уровне\n !ВНИМАНИЕ высокая степень дивиации!")
        elif (criteriaActivity > 4 and criteriaConcen > 4):
            result[3].append(f"Стоит обратить внимание так как Активность,Вовлеченность - на высшем уровне\n !ВНИМАНИЕ высокая степень дивиации!")
        elif (criteriaActivity > 4 and criteriaLiter > 4):
            result[3].append(f"Стоит обратить внимание так как Активность,Грамотность - на высшем уровне\n !ВНИМАНИЕ высокая степень дивиации!")
        elif (criteriaConcen > 4 and criteriaLiter > 4):
            result[3].append(f"Стоит обратить внимание так как Вовлеченность,Грамотность - на высшем уровне\n !ВНИМАНИЕ высокая степень дивиации!")
        else:
            result[3].append(f"НЕ РЕКОМЕНДУЮ на основании слишком высокой степени Дивиации")
    result[3].append("Не забудьте заглянуть в тест Люшера!")
    result[0].append("--- %s секунд на анализ профиля ---" % (int(time.time() - startTime)))
    return result
