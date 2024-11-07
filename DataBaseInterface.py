import sqlite3
import json


def addUser(lastName, firstName, birthDate, friendCount, totalPosts, totalComments, totalLikes,
            profanityCount, errorsCount, extremistWordCount, threatWordCount, groupThemes, userRating, userLink):
    groupThemesJson = json.dumps(groupThemes)
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scan_history (
            lastName, firstName, birthDate, friendCount, totalPosts, totalComments, totalLikes,
            profanityCount, errorsCount, extremistWordCount,
            threatWordCount, groupThemes, userRating, userLink
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        lastName,  # Собираю
        firstName,  # Собираю
        birthDate,  # Собираю
        friendCount,  # Собираю
        totalPosts,  # Собираю
        totalComments,  # Собираю
        totalLikes,  # Собираю
        profanityCount,  # Собираю
        errorsCount,  # Собираю
        extremistWordCount,  # Собираю
        threatWordCount,  # Собираю
        groupThemesJson,  # Не собираю
        userRating,  # Не собираю
        userLink
    ))
    conn.commit()
    conn.close()


def getLast5Users():
    """
    Возвращает последние 5 пользователей с полями id, lastName, firstName, birthDate.
    """
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT userID, lastName, firstName, birthDate
        FROM scan_history
        ORDER BY userID DESC
        LIMIT 5
    ''')
    users = cursor.fetchall()
    conn.close()
    for user in users:
        print(user)
    return users


def getUserById(user_id):
    """
    Возвращает все данные пользователя по заданному id.

    :param user_id: ID пользователя
    :return: Кортеж с данными пользователя или None, если пользователь не найден
    """
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT *
        FROM scan_history
        WHERE userID = ?
    ''', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def deleteUserById(user_id):
    """
    Удаляет пользователя из базы данных по заданному id.

    :param user_id: ID пользователя для удаления
    :return: True, если пользователь был удалён, иначе False
    """
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM scan_history
        WHERE userID = ?
    ''', (user_id,))
    conn.commit()
    changes = cursor.rowcount
    conn.close()
    return changes > 0


print(getUserById(4))
