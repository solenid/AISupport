import sqlite3

def initializeDB():
    """
    Инициализирует базу данных и создаёт таблицу scan_history с новой структурой.
    """
    try:
        with sqlite3.connect('history.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE scan_history (
                    userID INTEGER PRIMARY KEY AUTOINCREMENT,
                    lastName TEXT NOT NULL,
                    firstName TEXT NOT NULL,
                    birthDate TEXT,
                    criteriaCommun TEXT NOT NULL,
                    criteriaLiter TEXT NOT NULL,
                    criteriaActivity TEXT NOT NULL,
                    criteriaConcen TEXT NOT NULL,
                    criteriaRedFlag TEXT NOT NULL,
                    result TEXT NOT NULL,
                    link TEXT NOT NULL
                )
            ''')
            conn.commit()
            print("База данных 'history.db' и таблица 'scan_history' успешно созданы с новой структурой.")
    except sqlite3.Error as e:
        print(f"Произошла ошибка при инициализации базы данных: {e}")

def addUser(lastName, firstName, birthDate, criteriaCommun, criteriaLiter,
             criteriaActivity, criteriaConcen, criteriaRedFlag, result, link):
    """
    Добавляет нового пользователя в таблицу scan_history.
    """
    try:
        initializeDB()
        with sqlite3.connect('history.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO scan_history (
                    lastName, firstName, birthDate, 
                    criteriaCommun, criteriaLiter, criteriaActivity, 
                    criteriaConcen, criteriaRedFlag, result, link
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                lastName,
                firstName,
                birthDate,
                criteriaCommun,
                criteriaLiter,
                criteriaActivity,
                criteriaConcen,
                criteriaRedFlag,
                result,
                link
            ))
            conn.commit()
            print("Пользователь успешно добавлен.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")

def getLast5Users():
    """
    Возвращает последние 5 добавленных пользователей.
    """
    try:
        with sqlite3.connect('history.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM scan_history
         ORDER BY userID DESC
                        LIMIT 5
                    ''')
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Ошибка при получении пользователей: {e}")
        return []

def getUserById(user_id):
    """
    Возвращает пользователя по его userID.
    """
    try:
        with sqlite3.connect('history.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                        SELECT * FROM scan_history
                        WHERE userID = ?
                    ''', (user_id,))
            row = cursor.fetchone()
            return row
    except sqlite3.Error as e:
        print(f"Ошибка при получении пользователя: {e}")
        return None

def deleteUserById(user_id):
    """
    Удаляет пользователя по его userID.
    """
    try:
        with sqlite3.connect('history.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                        DELETE FROM scan_history
                        WHERE userID = ?
                    ''', (user_id,))
            conn.commit()
            if cursor.rowcount:
                print(f"Пользователь с ID {user_id} успешно удалён.")
            else:
                print(f"Пользователь с ID {user_id} не найден.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении пользователя: {e}")
