from vk_api.exceptions import VkApiError
import datetime

def get_posts_for_last_year(vk, user_id):
    one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

    posts = []
    try:
        response = vk.wall.get(owner_id=user_id, count=100, filter='owner', extended=0, offset=0)
        total_posts = response['count']

        for offset in range(0, total_posts, 100):
            batch = vk.wall.get(owner_id=user_id, count=100, filter='owner', offset=offset)['items']
            for post in batch:
                post_date = datetime.datetime.fromtimestamp(post['date'])
                if post_date >= one_year_ago:
                    posts.append(post)
                else:
                    return posts
    except VkApiError as e:
        print(f"Ошибка при получении постов: {e}")
    return posts
