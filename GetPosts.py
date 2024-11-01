from vk_api.exceptions import VkApiError
import datetime

def getPostsForLastYear(vk, userID):
    yearAgo = datetime.datetime.now() - datetime.timedelta(days=365)

    posts = []
    try:
        response = vk.wall.get(owner_id=userID, count=100, filter='owner', extended=0, offset=0)
        totalPosts = response['count']

        for offset in range(0, totalPosts, 100):
            batch = vk.wall.get(owner_id=userID, count=100, filter='owner', offset=offset)['items']
            for post in batch:
                postDate = datetime.datetime.fromtimestamp(post['date'])
                if postDate >= yearAgo:
                    posts.append(post)
                else:
                    return posts
    except VkApiError as e:
        print(f"Ошибка при получении постов: {e}")
    return posts
