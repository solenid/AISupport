import vk_api
import time
from CheckSpelling import *
from WordsFinder import *
from GetPosts import *
from GetToken import *
from UsersGet import *
from GreenWordsFinder import *

TOKEN = getToken()


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


def getInfoFromVK(userID: str, serviceToken, userToken):

    # Флаги оценок
    criteriaCommun = 0 # Общительность
    criteriaLiter = 0 # Грамотность
    criteriaConcen = 0 # Концентрация
    criteriaActivity = 0 # Активность
    criteriaRedFlag = 0 # Ред флаги

    result = [["ОБЩАЯ ИНФОРМАЦИЯ: ",f"Используемый user_id: {userID}"], ["RED FLAGs: "],["GREEN FLAGs: "]] # 0 - общая | 1 - red flags | 2 - green flags
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
        #Оценка общительности
        if friendsNum > 100:
            if friendsNum > 200:
                criteriaCommun += 2
            else:
                criteriaCommun += 1


    # 2. Получение кол-ва постов за год
    posts = getPostsForLastYear(vk, userID)
    numPosts = len(posts)
    result[0].append(f"Всего постов за год: {numPosts}")
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

        # Оценка общительности
        if totalComments > (friendsNum*(0.2)):
            if totalComments > (friendsNum*(0.5)):
                criteriaCommun += 2
            else:
                criteriaCommun += 1

        # 4. Общее количество лайков за год
        totalLikes = getTotalLikes(posts)
        result[0].append(f"Общее количество лайков за год: {totalLikes}")

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
                #Оценка грамотности (точности)
                if (errCount) != 0:
                    if errCount/totalWords < 0.1:
                        criteriaLiter = 4
                else:
                    criteriaLiter = 6


                # 6. Количество матерных постов
                totalForbiddenCount = 0
                totalForbiddenCount = forbiddenWordsSearch(postsText, totalForbiddenCount)
                result[1].append(f"Общее кол-во матерных постов: {totalForbiddenCount}")

                # Оценка дивиации
                if totalForbiddenCount / numPosts > 0.15:
                    if totalForbiddenCount / numPosts > 0.25:
                        criteriaRedFlag += 2
                    else:
                        criteriaRedFlag += 1

                # 6+ Количество постов по теме PR менеджемента
                totalGFWordCount = 0
                totalGFWordCount = greenWordInPosts(postsText, totalGFWordCount)
                result[2].append(f"Общее кол-во релевантных постов: {totalGFWordCount}")



                # 7. Количество экстремистких слов в постах
                totalForbiddenCount = 0
                for text in postsText:
                    forbiddenCount = countExtremismWords(text)
                    totalForbiddenCount += forbiddenCount
                result[1].append(f"Общее кол-во экстремистских слов в постах: {totalForbiddenCount}")

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
                # Оценка дивиации
                if totalForbiddenCount / totalWords > 0.05:
                    if totalForbiddenCount / totalWords > 0.15:
                        criteriaRedFlag += 2
                    else:
                        criteriaRedFlag += 1
            else:
                # Если слов все-таки нет
                result[0].append(f"Отсутствуют текстовые посты")
                criteriaRedFlag = -1
                criteriaLiter = -1
        else:
            result[0].append(f"Отсутствуют текстовые посты")
            criteriaRedFlag = -1
            criteriaLiter = -1
    else:
        result[0].append(f"Отсутствуют посты")
        criteriaRedFlag = -1
        criteriaLiter = -1
    # 9. Тематики групп пользователя
    vk = getVKSession(userToken)
    themes = getGroupsTheme(vk, userID)[:5]
    result[0].append("Топ 5 тематик групп пользователя:")
    for theme in themes:
        result[0].append(f"- {theme}")

    #10 ОЦЕНКА пользователя
    result[2].append(f"Общительность: {getCriteriaGrade(criteriaCommun)}")
    result[2].append(f"Грамотность: {getCriteriaGrade(criteriaLiter)}")
    result[2].append(f"Активность: {getCriteriaGrade(criteriaActivity)}")
    result[1].append(f"Степень дивиации: {getCriteriaGrade(criteriaRedFlag)}")

    result[0].append("--- %s секунд на анализ профиля ---" % (int(time.time() - startTime)))
    return result
