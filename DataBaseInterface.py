import sqlite3
import json

conn = sqlite3.connect('history.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS scan_history (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        friend_count INTEGER NOT NULL CHECK(friend_count >= 0),
        total_posts INTEGER NOT NULL CHECK(total_posts >= 0),
        total_comments INTEGER NOT NULL CHECK(total_comments >= 0),
        total_likes INTEGER NOT NULL CHECK(total_likes >= 0),
        profanity_count INTEGER NOT NULL DEFAULT 0 CHECK(profanity_count >= 0),
        extremist_word_count INTEGER NOT NULL DEFAULT 0 CHECK(extremist_word_count >= 0),
        threat_word_count INTEGER NOT NULL DEFAULT 0 CHECK(threat_word_count >= 0),
        group_themes TEXT,
        user_rating REAL CHECK(user_rating >= 0 AND user_rating <= 100),
        user_link TEXT NOT NULL
    )
''')


def addUser(lastName, firstName, friendCount, totalPosts, totalComments, totalLikes,
            profanityCount, extremistWordCount, threatWordCount, groupThemes, userRating, userLink):
    group_themes_json = json.dumps(groupThemes)

    cursor.execute('''
        INSERT INTO scan_history (
            lastName, firstName, friendCount, totalPosts, totalComments, totalLikes,
            profanityCount, extremistWordCount,
            threatWordCount, groupThemes, userRating, userLink
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        lastName,
        firstName,
        friendCount,
        totalPosts,
        totalComments,
        totalLikes,
        profanityCount,
        extremistWordCount,
        threatWordCount,
        groupThemes,
        userRating,
        userLink
    ))
    conn.commit()


def getUsers():
    cursor.execute('SELECT * FROM scan_history')
    row = cursor.fetchall()
    for user in row:
        user = list(user)
        user[10] = json.loads(user[10]) if user[10] else []
        print(user)


def delete_user():
    cursor.execute('DELETE FROM scan_history')
    conn.commit()


conn.close()
