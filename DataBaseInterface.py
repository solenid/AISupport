import sqlite3
import json

conn = sqlite3.connect('history.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS scan_history (
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
        user_rating REAL CHECK(user_rating >= 0 AND user_rating <= 100)
    )
''')


def add_user(last_name, first_name, friend_count, total_posts, total_comments, total_likes,
             profanity_count, extremist_word_count, threat_word_count, group_themes, user_rating):
    group_themes_json = json.dumps(group_themes)

    cursor.execute('''
        INSERT INTO scan_history (
            last_name, first_name, friend_count, total_posts, total_comments, total_likes,
            profanity_count, extremist_word_count,
            threat_word_count, group_themes, user_rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        last_name,
        first_name,
        friend_count,
        total_posts,
        total_comments,
        total_likes,
        profanity_count,
        extremist_word_count,
        threat_word_count,
        group_themes_json,
        user_rating
    ))
    conn.commit()


def get_users():
    cursor.execute('SELECT * FROM scan_history')
    row = cursor.fetchall()
    for user in row:
        user = list(user)
        user[9] = json.loads(user[9]) if user[9] else []
        print(user)


def delete_user():
    cursor.execute('DELETE FROM scan_history')


get_users()
conn.close()
