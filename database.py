import sqlite3


def create_table():
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS game_users"
                   "(user_name TEXT PRIMARY KEY NOT NULL DEFAULT 'Default',"
                   "password TEXT DEFAULT '',"
                   "games INTEGER DEFAULT 0,"
                   "score INTEGER DEFAULT 0,"
                   "highest_score INTEGER DEFAULT 0);")
    conn.commit()


def drop_table():
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE game_users;")
    conn.commit()


def add_user(user_name, password):
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM game_users WHERE user_name = ?;", (user_name,))
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO game_users (user_name, password) VALUES (?, ?);", (user_name, password))
        conn.commit()
        return True
    else:
        return False


def change_user_name(user_name, password, new_user_name):
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM game_users WHERE user_name = ? AND password = ?;", (user_name, password,))
    if cursor.fetchone() is not None:
        cursor.execute(
            f"UPDATE game_users SET user_name = ? WHERE user_name = ? AND password = ?;",
            (new_user_name, user_name, password,))
        conn.commit()
        return True

    else:
        return False


def increment_games(user_name):
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM game_users WHERE user_name = ?;", (user_name,))
    if cursor.fetchone() is not None:
        cursor.execute(f"UPDATE game_users SET games = games + 1 WHERE user_name = ?;", (user_name,))
        conn.commit()
        return True
    else:
        return False


def update_score(user_name, score):
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM game_users WHERE user_name = ?;", (user_name,))
    if cursor.fetchone() is not None:
        cursor.execute(
            f"UPDATE game_users SET score = score + ?, highest_score = max(highest_score, ?) "
            f"WHERE user_name = ?", (score, score, user_name,))
        conn.commit()
        return True

    else:
        return False


def login(user_name, password):
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM game_users WHERE user_name = ? AND password = ?;", (user_name, password,))
    if cursor.fetchone() is not None:
        return True
    else:
        return False
