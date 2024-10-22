import vk_api
import time
from CheckSpelling import *
from WordsFinder import *
from GetPosts import *
from GetToken import *

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

# def get_posts_photo(posts):
#     posts_photo = [post.get('photo', '') for post in posts]
#     return posts_photo

def get_publics_theme(vk, user_id):
    try:
        response = vk.groups.get(user_id=user_id, count=0)
        return response['count']
    except VkApiError as e:
        print(f"Ошибка при получении групп: {e}")
        return None


def get_groups_theme(vk, user_id):
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
                themes.add(activity)
        offset += count
    return list(themes)


def get_info(user_id: str):
    result = [f"Используемый user_id: {user_id}"]
    start_time = time.time()
    vk = get_vk_session(TOKEN)
    if vk is None:
        exit()
    # 1. Количество друзей
    number_of_friends = get_number_of_friends(vk, user_id)
    if number_of_friends is not None:
        result.append(f"Количество друзей пользователя: {number_of_friends}")

    # 2. Получение кол-ва постов за год
    posts = get_posts_for_last_year(vk, user_id)
    result.append(f"Всего постов за год: {len(posts)}")

    # 3. Общее количество комментариев за год
    total_comments = get_total_comments(posts)
    result.append(f"Общее количество комментариев за год: {total_comments}")

    # 4. Общее количество лайков за год
    total_likes = get_total_likes(posts)
    result.append(f"Общее количество лайков за год: {total_likes}")

    # 5. Тексты постов за год и проверка на ошибки
    posts_text = get_posts_text(posts)
    errors_counts = 0
    for idx, text in enumerate(posts_text, 1):
        errors = check_spelling(text)
        if errors:
            errors_counts += len(errors)
    result.append(f"Общее кол-во ошибок в постах за год : {errors_counts}")

    # 6. Количество матерных слов в постах
    total_forbidden_count = 0
    forbidden_words_search(posts_text, total_forbidden_count)
    result.append(f"Общее кол-во матерных слов в постах: {total_forbidden_count}")

    # 7. Количество экстремистких слов в постах
    total_forbidden_count = 0
    for text in posts_text:
        forbiddenCount = count_extremism_words(text)
        total_forbidden_count += forbiddenCount
    result.append(f"Общее кол-во экстремистких слов в постах: {total_forbidden_count}")

    # 8. Количество слов-угроз в постах
    total_forbidden_count = 0
    for text in posts_text:
        forbiddenCount = count_threat_words(text)
        total_forbidden_count += forbiddenCount
    result.append(f"Общее кол-во слов-угроз в постах: {total_forbidden_count}")

    # 9. Тематики групп пользователя
    themes = get_groups_theme(vk, user_id)
    result.append("Тематики групп пользователя:")
    for theme in themes:
        result.append(f"- {theme}")
    result.append("--- %s секунд на анализ профиля ---" % (int(time.time() - start_time)))
    return result
