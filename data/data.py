from enum import Enum
# DATA
ACCESS_TOKEN = 'f5047191f5047191f5047191caf624eadeff504f5047191920feda5943381a1caa2ddf2' # Замените 'YOUR_ACCESS_TOKEN' на ваш токен доступа
USER_ID = 'aidkhall'
USER_ID_INTEGER = None
COUNT_FRIEND = None
COUNT_POSTS = 10 # количество постов
FILTER = 'owner' # Записи владельца или других пользователей
OFFSET = 0 # Сдвиг
class CHOICE(Enum):
    NONE = 'none'
    TEXT = 'text'
    PHOTO = 'photo'


# URL
urlWallGetById = 'https://api.vk.com/method/wall.get'
urlUtilsResolveScreenName = 'https://api.vk.com/method/utils.resolveScreenName'
urlFriendsGet = 'https://api.vk.com/method/friends.get'


# Параметры запроса
paramsForWallGetById = {
    'access_token': ACCESS_TOKEN,
    'owner_id': f'{USER_ID}',
    'offset': f'{OFFSET}',
    'count': f'{COUNT_POSTS}',
    'filter': f'{FILTER}',
    'v': '5.131'  # Версия API
}
paramsForUtilsResolveScreenName = {
    'access_token': ACCESS_TOKEN,
    'screen_name': USER_ID,
    'v': '5.131'  # Версия API
}

paramsForFriendsGet = {
    'access_token': ACCESS_TOKEN,
    'user_id': USER_ID_INTEGER,
    'order': 'random',
    'fields': '',
    'v': '5.131'  # Версия API
}