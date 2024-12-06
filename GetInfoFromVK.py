import vk_api
import time
import tkinter as tk

# import Main
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
    while True: # Зачем?
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

def getBase(vk, userID):
    result = []
    fields = 'status, bdate, universities, interests, schools'
    try:
        response = vk.users.get(user_ids=userID, fields=fields)
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

def getPhotoCount(vk, userID):
    resPhotos = 0
    try:
        dataForWallGetById = vk.wall.get(owner_id=userID, filter='owner', extended=0, offset=0)
    except VkApiError as e:
        print(f"Ошибка при получении постов: {e}")
        return resPhotos

    for elements in dataForWallGetById['items']:
        for element in elements['attachments']:
            if ('photo' in element):
                resPhotos += 1
    return resPhotos

def getInfoFromVK(userID: str, serviceToken, userToken, type):
    # Флаги оценок
    criteriaCommun = 0  # Общительность
    criteriaLiter = 0  # Грамотность
    criteriaConcen = 0  # Концентрация
    criteriaActivity = 0  # Активность
    criteriaRedFlag = 0  # Ред флаги
    #Критерии
    # Грамотность
    midErrNum = 0.1
    greatErrNum = 0.25
    # Остальное зависит от типа
    if type == 0: #Человек природа
        # Ш-Общительность
        midSFrNum = 30
        greatSFrNum = 70
        midPhotoNum = 1
        greatPhotoNum = 2
        # Вовлеченность (все в процентах)
        midRelSubNum = 0.6
        greatRelSubNum = 0.75
        minRelPostNum = 0.6
        greatRelPostNum = 0.75
        # Активность
        midActivPostNum = 3
        greatActivPostNum = 5
        midAComNum = 15
        greatAComNum = 45
        midALikeNum = 40
        greatALikeNum = 90
    elif type == 1 or type == -1: #Человек человек (Здесь находится наш основной путь PR)
        # Ш-Общительность
        midSFrNum = 100
        greatSFrNum = 200
        midPhotoNum = 5
        greatPhotoNum = 15
        # Вовлеченность (все в процентах)
        midRelSubNum = 0.5
        greatRelSubNum = 0.7
        minRelPostNum = 0.5
        greatRelPostNum = 0.7
        # Активность
        midActivPostNum = 6
        greatActivPostNum = 10
        midAComNum = 25
        greatAComNum = 75
        midALikeNum = 100
        greatALikeNum = 150
    elif type == 2: #Человек знак
        # Ш-Общительность
        midSFrNum = 40
        greatSFrNum = 80
        midPhotoNum = 2
        greatPhotoNum = 3
        # Вовлеченность (все в процентах)
        midRelSubNum = 0.7
        greatRelSubNum = 0.85
        minRelPostNum = 0.7
        greatRelPostNum = 0.85
        # Активность
        midActivPostNum = 4
        greatActivPostNum = 6
        midAComNum = 20
        greatAComNum = 50
        midALikeNum = 55
        greatALikeNum = 120
    elif type == 3: #Человек техника
        # Ш-Общительность
        midSFrNum = 35
        greatSFrNum = 75
        midPhotoNum = 1
        greatPhotoNum = 2
        # Вовлеченность (все в процентах)
        midRelSubNum = 0.65
        greatRelSubNum = 0.85
        minRelPostNum = 0.65
        greatRelPostNum = 0.85
        # Активность
        midActivPostNum = 4
        greatActivPostNum = 5
        midAComNum = 15
        greatAComNum = 45
        midALikeNum = 40
        greatALikeNum = 90
    elif type == 4: #Человек босс художки
        # Ш-Общительность
        midSFrNum = 120
        greatSFrNum = 200
        midPhotoNum = 7
        greatPhotoNum = 15
        # Вовлеченность (все в процентах)
        midRelSubNum = 0.7
        greatRelSubNum = 0.90
        minRelPostNum = 0.7
        greatRelPostNum = 0.90
        # Активность
        midActivPostNum = 7
        greatActivPostNum = 12
        midAComNum = 30
        greatAComNum = 80
        midALikeNum = 125
        greatALikeNum = 175
    else:
        print("Неопределенный тип пользователя!")
        exit()


    result = [["ОБЩАЯ ИНФОРМАЦИЯ: ",f"Используемый user_id: {userID}"], ["RED FLAGs: "],["GREEN FLAGs: "],["Рекомендации:"], ["Тест Герчикова: "]] # 0 - общая | 1 - red flags | 2 - green flags | 3 - рекомендация | 4 - Герчиков
    startTime = time.time()
    vk = getVKSession(serviceToken)
    if vk is None:
        exit()

    base = getBase(vk, userID)
    for res in base:
        result[0].append(res)
    # 1. Количество друзей
    friendsNum = getNumberOfFriends(vk, userID)
    if friendsNum is not None:
        result[0].append(f"Количество друзей пользователя: {friendsNum}")
        #Оценка общительности
        if friendsNum > midSFrNum:
            if friendsNum > greatSFrNum:
                criteriaCommun += 3
            else:
                criteriaCommun += 2

    photosNum = getPhotoCount(vk, userID)
    if photosNum > midPhotoNum:
        if photosNum > greatPhotoNum:
            criteriaCommun += 3
        else:
            criteriaCommun += 2

    # 2. Получение кол-ва постов за год
    posts = getPostsForLastYear(vk, userID)
    numPosts = len(posts)
    result[0].append(f"Всего постов за год: {numPosts}")
    if numPosts > 0:

        # Оценка Активности
        if numPosts > midActivPostNum:
            if numPosts > greatActivPostNum:
                criteriaActivity = 2
            else:
                criteriaActivity = 1

        # 3. Общее количество комментариев за год
        totalComments = getTotalComments(posts)
        result[0].append(f"Общее количество комментариев за год: {totalComments}")
        # Оценка Активности (общ)
        if totalComments > (midAComNum):
            if totalComments > (greatAComNum):
                criteriaActivity += 2
            else:
                criteriaActivity += 1

        # 4. Общее количество лайков за год
        totalLikes = getTotalLikes(posts)
        result[0].append(f"Общее количество лайков за год: {totalLikes}")

        # Оценка Активность  (общ)
        if totalLikes > (midALikeNum):
            if totalLikes > (greatALikeNum):
                criteriaActivity += 2
            else:
                criteriaActivity += 1

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
                #Оценка грамотности (точности)
                if errCount/totalWords < greatErrNum:
                    if errCount/totalWords < midErrNum:
                        criteriaLiter = 6
                    else:
                        criteriaLiter = 4
                else:
                    criteriaLiter = 0

                totalForbiddenCount = 0 # 6. Количество матерных постов
                totalGFWordCount = 0 # 6+ Количество постов по теме PR менеджемента
                searcRes = WordsSearch(postsText, totalGFWordCount, totalForbiddenCount, type)
                totalForbiddenCount = searcRes[0]
                totalGFWordCount = searcRes[1]
                result[1].append(f"Общее кол-во матерных постов: {totalForbiddenCount}")
                result[2].append(f"Общее кол-во релевантных постов: {totalGFWordCount}")

                # Оценка дивиации
                if totalForbiddenCount / numPosts > 0:
                    if totalForbiddenCount / numPosts > 0.1:
                        criteriaRedFlag += 6
                    else:
                        criteriaRedFlag += 4

                # Оценка сосредоточенности Вовлеченность
                if totalGFWordCount > minRelPostNum:
                    if totalGFWordCount / numPosts > greatRelPostNum:
                        criteriaConcen += 3
                    else:
                        criteriaConcen += 1.5


                # 7. Количество экстремистких слов в постах
                totalForbiddenCount = 0
                for text in postsText:
                    forbiddenCount = countExtremismWords(text)
                    totalForbiddenCount += forbiddenCount
                result[1].append(f"Общее кол-во экстремистских слов в постах: {totalForbiddenCount}")

                # Оценка дивиации
                if totalForbiddenCount / totalWords > 0.01:
                    if totalForbiddenCount / totalWords > 0.05:
                        criteriaRedFlag += 6
                    else:
                        criteriaRedFlag += 4

                # 8. Количество слов-угроз в постах
                totalForbiddenCount = 0
                for text in postsText:
                    forbiddenCount = countThreatWords(text)
                    totalForbiddenCount += forbiddenCount
                result[1].append(f"Общее кол-во слов-угроз в постах: {totalForbiddenCount}")
                # Оценка дивиации
                if totalForbiddenCount / totalWords > 0:
                    if totalForbiddenCount / totalWords > 0.05:
                        criteriaRedFlag += 6
                    else:
                        criteriaRedFlag += 4
            else:
                # Если слов все-таки нет
                result[0].append(f"Отсутствуют текстовые посты")
                criteriaConcen = -1
                criteriaRedFlag = -1
                criteriaLiter = -1
        else:
            result[0].append(f"Отсутствуют текстовые посты")
            criteriaConcen = -1
            criteriaRedFlag = -1
            criteriaLiter = -1
    else:
        result[0].append(f"Отсутствуют посты")
        criteriaConcen = -1
        criteriaRedFlag = -1
        criteriaLiter = -1
    # 9. Тематики групп пользователя
    vk = getVKSession(userToken)
    themes = getGroupsTheme(vk, userID) #Топ 5 тематик пользователя

    totalGFWordTheme = 0  # Количество тематик релевантных
    searcRes = WordsSearch(themes, totalGFWordTheme, 0, type)
    totalGFWordTheme = searcRes[1]
    #Оценка концентрации
    if totalGFWordTheme > midRelSubNum:
        if totalGFWordTheme > greatRelSubNum:
            criteriaConcen += 3
        else:
            criteriaConcen += 1.5

    result[0].append("Топ 5 тематик групп пользователя:")
    for theme in themes [:5]:
        result[0].append(f"- {theme}")

    #10 ОЦЕНКА пользователя
    result[2].append(f"Общительность: {getCriteriaGrade(criteriaCommun)}")
    result[2].append(f"Грамотность: {getCriteriaGrade(criteriaLiter)}")
    result[2].append(f"Активность: {getCriteriaGrade(criteriaActivity)}")
    result[2].append(f"Вовлеченность: {getCriteriaGrade(criteriaConcen)}")
    result[1].append(f"Степень дивиации: {getCriteriaGrade(criteriaRedFlag)}")

    dataDB.append(criteriaCommun)
    dataDB.append(criteriaLiter)
    dataDB.append(criteriaActivity)
    dataDB.append(criteriaConcen)
    dataDB.append(criteriaRedFlag)

    if criteriaRedFlag <= 5:
        #Полностью рекомендую
        if criteriaCommun > 4 and criteriaLiter > 4 and criteriaActivity > 4 and criteriaConcen > 4:
            text = "ПОЛНОСТЬЮ РЕКОМЕНДУЮ на основании:\n> Общительность, Грамотность, Активность, Вовлеченность - на высшем уровне"
            result[3].append(text)
            dataDB.append(text)
        #Рекомендую
        elif criteriaCommun > 2 and criteriaLiter > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Общительность, Грамотность - на высоком/среднем уровне"
            result[3].append(text)
            dataDB.append(text)
        elif criteriaActivity > 2 and criteriaConcen > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Активность, Вовлеченность - на высоком/среднем уровне"
            result[3].append(text)
            dataDB.append(text)
        elif criteriaCommun > 2 and criteriaActivity > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Общительность, Активность- на высоком/среднем уровне"
            result[3].append(text)
            dataDB.append(text)
        elif criteriaCommun > 2 and criteriaConcen > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Общительность, Вовлеченность - на высоком/среднем уровне"
            result[3].append(text)
            dataDB.append(text)
        elif criteriaLiter > 2 and criteriaActivity > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Грамотность,Активность - на высоком/среднем уровне"
            result[3].append(text)
            dataDB.append(text)
        elif criteriaLiter > 2 and criteriaConcen > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Грамотность, Вовлеченность - на высоком/среднем уровне"
            result[3].append(text)
            dataDB.append(text)
        # Рекомендую, НО
        elif criteriaCommun > 2 and criteriaLiter > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Общительность, Грамотность - на высоком/среднем уровне\n> ! ОБРАТИТЕ ВНИМАНИЕ, СРЕДНИЙ УРОВЕНЬ ДИВИАЦИИ !"
            result[3].append(text)
            dataDB.append(text)
        elif criteriaActivity > 2 and criteriaConcen > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Активность, Вовлеченность - на высоком/среднем уровне\n> ! ОБРАТИТЕ ВНИМАНИЕ. СРЕДНИЙ УРОВЕНЬ ДИВИАЦИИ !"
            result[3].append(text)
            dataDB.append(text)
        elif criteriaCommun > 2 and criteriaActivity > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Общительность, Активность- на высоком/среднем уровне\n> ! ОБРАТИТЕ ВНИМАНИЕ, СРЕДНИЙ УРОВЕНЬ ДИВИАЦИИ !"
            result[3].append(text)
            dataDB.append(text)
        elif criteriaCommun > 2 and criteriaConcen > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Общительность, Вовлеченность - на высоком/среднем уровне\n> ! ОБРАТИТЕ ВНИМАНИЕ, СРЕДНИЙ УРОВЕНЬ ДИВИАЦИИ !"
            result[3].append(text)
            dataDB.append(text)
        elif criteriaLiter > 2 and criteriaActivity > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Грамотность,Активность - на высоком/среднем уровне\n> ! ОБРАТИТЕ ВНИМАНИЕ, СРЕДНИЙ УРОВЕНЬ ДИВИАЦИИ !"
            result[3].append(text)
            dataDB.append(text)
        elif criteriaLiter > 2 and criteriaConcen > 2 and criteriaRedFlag <= 2:
            text = "РЕКОМЕНДУЮ на основании:\n> Грамотность, Вовлеченность - на высоком/среднем уровне\n> ! ОБРАТИТЕ ВНИМАНИЕ, СРЕДНИЙ УРОВЕНЬ ДИВИАЦИИ !"
            result[3].append(text)
            dataDB.append(text)
        # Не рекомендую
        else:
            text = "НЕ РЕКОМЕНДУЮ на основании отсутвия необходимых качеств"
            result[3].append(text)
            dataDB.append(text)
    else:
        # Не рекомендую
        result[3].append(f"НЕ РЕКОМЕНДУЮ на основании слишком высокой степени Дивиации")


    #Блок Герчикова
    #НАДО ПРИДУМАТЬ КУДА ЭТО СКЛАДЫВАТЬ, ВЕРОЯТНО ОТДЕЛЬНАЯ КНОПКА И ОТДЕЛЬНАЯ ВКЛАДКА
    #НО Я БЫ ПЕРЕИМЕНОВАЛ ВКЛАДКУ С ЛЮЩЕРОМ И ПИСАЛ ТУДА
    resultGerchikov = ""
    if criteriaRedFlag > 4:
        resultGerchikov += "Избегательный тип\nХарактеризуется отсутствием у сотрудника четких ценностей и профессиональных ориентиров. Поощрение и наказание в данном случае могут быть сложными, так как такие сотрудники могут не реагировать на обычные стимулы.\n\n"
    if criteriaConcen > 4:
        resultGerchikov += "Профессиональный тип\nХарактеризуется стремлением сотрудника к профессиональному росту и развитию, к приобретению новых знаний и навыков. Поощрением может служить возможность участия в профессиональных семинарах, тренингах, курсах повышения квалификации.\n\n"
    if gerchikovKeyWords(themes, True) > 3:
        resultGerchikov += "Инструментальный тип\nСотрудник рассматривает работу как инструмент для достижения определенных целей, таких как материальное благополучие. Поощрением для таких сотрудников может стать премия, бонус или повышение зарплаты.\n\n"
    if numPosts > 0:
        if totalWords > 0:
            if gerchikovKeyWords(postsText, False) > 3:
                resultGerchikov += "Патриотический тип\nОснован на любви сотрудника к своей компании и стремлении приносить ей пользу. Поощрением для таких сотрудников может служить публичное признание их вклада в успех компании, награды за лояльность и долгосрочную службу.\n\n"
    if len(resultGerchikov) > 0:
        result[4].append(resultGerchikov)
    else:
        resultGerchikov += "Инструментальный тип\nСотрудник рассматривает работу как инструмент для достижения определенных целей, таких как материальное благополучие. Поощрением для таких сотрудников может стать премия, бонус или повышение зарплаты.\n\n"
        result[4].append(resultGerchikov)

    result[3].append("Не забудьте заглянуть в тест Люшера!")
    result[0].append("--- %s секунд на анализ профиля ---" % (int(time.time() - startTime)))

    dataDB.append(f'https://vk.com/id{userID}')
    print(dataDB)
    try:
        addUser(dataDB[0], dataDB[1], dataDB[2], dataDB[3], dataDB[4],
                dataDB[5], dataDB[6], dataDB[7], dataDB[8], dataDB[9])
    except Exception as e:
        print(f"Произошла ошибка при добавления пользователя в базу данных: {e}")
    print("Очистка массива ...")
    dataDB.clear()
    print("Массив Очищен")

    # Main.statusLoad = 1

    return result
