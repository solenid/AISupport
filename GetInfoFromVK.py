import vk_api
import time
from CheckSpelling import *
from WordsFinder import *
from GetPosts import *
from GetToken import *
from UsersGet import *

TOKEN = get_token()


def get_vk_session(token):
    try:
        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()
        return vk
    except VkApiError as e:
        print(f"Ошибка при подключении к VK API: {e}")
        return None


def get_number_of_friends(vk, user_id):
    try:
        response = vk.friends.get(user_id=user_id, count=0)
        return response['count']
    except VkApiError as e:
        print(f"Ошибка при получении друзей: {e}")
        return None


def get_total_comments(posts):
    total_comments = sum(post.get('comments', {}).get('count', 0) for post in posts)
    return total_comments


def get_total_likes(posts):
    total_likes = sum(post.get('likes', {}).get('count', 0) for post in posts)
    return total_likes


def get_posts_text(posts):
    posts_text = [post.get('text', '') for post in posts]
    return posts_text

def get_publics_theme(vk, user_id):
    try:
        response = vk.groups.get(user_id=user_id, count=0)
        return response['count']
    except VkApiError as e:
        print(f"Ошибка при получении групп: {e}")
        return None

def get_criteria_grade(score):
    result = "Низкая"
    if score > 2:
        if score > 4:
            result = "Высокая"
        else:
            result = "Средняя"
    elif score < 0:
        result = "Не определено" #\n(веротяно нет постов или слов в них)"
    return result

def get_groups_theme(vk, user_id):
    dictionaryThemes = {}
    themes = set()
    offset = 0
    count = 1000
    while True:
        try:
            response = vk.groups.get(
                user_id=user_id,
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
            if activity:
                if activity in dictionaryThemes:
                    dictionaryThemes[f'{activity}'] += 1
                else:
                    dictionaryThemes[f'{activity}'] = 1
                # themes.add(activity)
        offset += count
    sorted_dict = {key: value for key,
    value in sorted(dictionaryThemes.items(),
                    key=lambda item: item[1], reverse=True)}
    return list(sorted_dict.keys())


def get_info(user_id: str, SERVICE_TOKEN, USER_TOKEN):

    # Флаги оценок
    criteriaCommun = 0 # Общительность
    criteriaLiter = 0 # Грамотность
    criteriaConcen = 0 # Концентрация
    criteriaActivity = 0 # Активность
    criteriaRedFlag = 0 # Ред флаги

    result = [f"Используемый user_id: {user_id}"]
    start_time = time.time()
    vk = get_vk_session(SERVICE_TOKEN)
    if vk is None:
        exit()

    base = GetBase(vk, user_id)
    for res in base:
        result.append(res)
    # 1. Количество друзей
    number_of_friends = get_number_of_friends(vk, user_id)
    if number_of_friends is not None:
        result.append(f"Количество друзей пользователя: {number_of_friends}")
        #Оценка общительности
        if number_of_friends > 100:
            if number_of_friends > 200:
                criteriaCommun += 2
            else:
                criteriaCommun += 1


    # 2. Получение кол-ва постов за год
    posts = get_posts_for_last_year(vk, user_id)
    numPosts = len(posts)
    result.append(f"Всего постов за год: {numPosts}")
    if numPosts > 0:

        # Оценка Активности
        if numPosts > 2:
            if numPosts > 6:
                criteriaActivity = 6
            else:
                criteriaActivity = 4

        # 3. Общее количество комментариев за год
        total_comments = get_total_comments(posts)
        result.append(f"Общее количество комментариев за год: {total_comments}")

        # Оценка общительности
        if total_comments > (number_of_friends*(0.2)):
            if total_comments > (number_of_friends*(0.5)):
                criteriaCommun += 2
            else:
                criteriaCommun += 1

        # 4. Общее количество лайков за год
        total_likes = get_total_likes(posts)
        result.append(f"Общее количество лайков за год: {total_likes}")

        # Оценка общительности
        if total_likes > (number_of_friends*(0.50)):
            if total_likes > (number_of_friends*(0.75)):
                criteriaCommun += 2
            else:
                criteriaCommun += 1

        #!Если есть текст в постах
        posts_text = get_posts_text(posts)
        if posts_text:
            # 5. Тексты постов за год и проверка на ошибки
            errors_counts = 0
            total_words = 0
            for idx, text in enumerate(posts_text, 1):
                total_words += len(text.split())
                errors = check_spelling(text)
                if errors:
                    errors_counts += len(errors)
            #!Если есть текст в постах СНОВА????????
            if (total_words) > 0:
                result.append(f"Общее кол-во ошибок в постах за год : {errors_counts}")
                #Оценка грамотности (точности)
                if (errors_counts) != 0:
                    if errors_counts/total_words < 0.1:
                        criteriaLiter = 4
                else:
                    criteriaLiter = 6


                # 6. Количество матерных постов
                total_forbidden_count = 0
                total_forbidden_count = forbidden_words_search(posts_text, total_forbidden_count)
                result.append(f"Общее кол-во матерных постов: {total_forbidden_count}")

                #Оценка дивиации
                if total_forbidden_count/numPosts > 0.15:
                    if total_forbidden_count/numPosts > 0.25:
                        criteriaRedFlag += 2
                    else:
                        criteriaRedFlag += 1

                # 7. Количество экстремистких слов в постах
                total_forbidden_count = 0
                for text in posts_text:
                    forbiddenCount = count_extremism_words(text)
                    total_forbidden_count += forbiddenCount
                result.append(f"Общее кол-во экстремистких слов в постах: {total_forbidden_count}")

                # Оценка дивиации
                if total_forbidden_count / total_words > 0.05:
                    if total_forbidden_count / total_words > 0.15:
                        criteriaRedFlag += 2
                    else:
                        criteriaRedFlag += 1

                # 8. Количество слов-угроз в постах
                total_forbidden_count = 0
                for text in posts_text:
                    forbiddenCount = count_threat_words(text)
                    total_forbidden_count += forbiddenCount
                result.append(f"Общее кол-во слов-угроз в постах: {total_forbidden_count}")
                # Оценка дивиации
                if total_forbidden_count / total_words > 0.05:
                    if total_forbidden_count / total_words > 0.15:
                        criteriaRedFlag += 2
                    else:
                        criteriaRedFlag += 1
            else:
                # Если слов все-таки нет
                result.append(f"Общее кол-во слов в постах: 0")
                criteriaRedFlag = -1
                criteriaLiter = -1
        else:
            result.append(f"Общее кол-во слов в постах: 0")
            criteriaRedFlag = -1
            criteriaLiter = -1
    # 9. Тематики групп пользователя
    vk = get_vk_session(USER_TOKEN)
    themes = get_groups_theme(vk, user_id)[:4]
    result.append("Топ 5 тематик групп пользователя:")
    for theme in themes:
        result.append(f"- {theme}")

    #10 ОЦЕНКА пользователя
    result.append(f"Общительность: {get_criteria_grade(criteriaCommun)}")
    result.append(f"Грамотность: {get_criteria_grade(criteriaLiter)}")
    result.append(f"Активность: {get_criteria_grade(criteriaActivity)}")
    result.append(f"Степень дивиации: {get_criteria_grade(criteriaRedFlag)}")
    result.append("--- %s секунд на анализ профиля ---" % (int(time.time() - start_time)))
    return result
