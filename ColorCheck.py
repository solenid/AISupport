from collections import namedtuple
from math import sqrt
import random
import requests
from io import BytesIO
try:
    from PIL import Image
except ImportError:
    import Image

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def getPoints(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(img, n=3):  # Изменено на img вместо filename
    img.thumbnail((200, 200))
    points = getPoints(img)
    clusters = kmeans(points, n, 1)
    rgbs = [list(map(int, c.center.coords)) for c in clusters]  # Используем list() для преобразования
    return rgbs #list(map(rtoh, rgbs))  # Используем list() для преобразования

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

def calculateCenter(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, minDiff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while True:
        plists = [[] for _ in range(k)]

        for p in points:
            smallestDistance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallestDistance:
                    smallestDistance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculateCenter(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < minDiff:
            break

    return clusters

def downloadImage(url):
    response = requests.get(url)
    response.raise_for_status()  # Проверка на ошибки
    return Image.open(BytesIO(response.content))

def colorCheck(url, nColors):
    try:
        image = downloadImage(url)
        return colorz(image, n=nColors)  # Обновите вызов функции colorz
    except Exception as e:
        print(f"Произошла ошибка: {e}")





# https://sun9-2.userapi.com/s/v1/ig2/TGqXypG7LCUd31ZnP_nuWZYhsUXk02VV1mI7i41PDLqTjQf9NK_Dqn28II34CdWiUPLFBgu6td3fYiLk7BRquyw2.jpg?quality=95&crop=4,248,1176,1176&as=32x32,48x48,72x72,108x108,160x160,240x240,360x360,480x480,540x540,640x640,720x720,1080x1080&ava=1&cs=50x50
# https://strogino.mos.ru/upload/medialibrary/005/cn52sgfb49fyxdslyf98hqx7lff63fbs/800px_Vk_logo.svg.png


# filename = 'calendar.png'  # Замените на путь к вашему изображению
# n_colors = 5  # Количество доминирующих цветов
#
# dominant_colors = colorz(filename, n=n_colors)
#
# print("Доминирующие цвета:")
# for color in dominant_colors:
#     print(color)  # Выводит цвета в формате HEX

# print("Доминирующие цвета:")
        #for color in dominant_colors:
        #     print(color)  # Выводит цвета в формате HEX
        #
        #   color = ''.join(color.split('#',1))
        #     print('RGB =', tuple(int(color[i:i + 2], 16) for i in (0, 2, 4)))

# url = 'https://sun9-2.userapi.com/s/v1/ig2/TGqXypG7LCUd31ZnP_nuWZYhsUXk02VV1mI7i41PDLqTjQf9NK_Dqn28II34CdWiUPLFBgu6td3fYiLk7BRquyw2.jpg?quality=95&crop=4,248,1176,1176&as=32x32,48x48,72x72,108x108,160x160,240x240,360x360,480x480,540x540,640x640,720x720,1080x1080&ava=1&cs=50x50'  # Замените на URL вашего изображения
# n_colors = 3  # Количество доминирующих цветов
