import sqlite3


def create_table():
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS bot_user"
                   "(chat_id integer PRIMARY KEY NOT NULL,"
                   "first_name TEXT DEFAULT '');")
    conn.commit()


def drop_table():
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE bot_user;")
    conn.commit()

def add_user(chat_id, first_name):
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()

    create_table()

    cursor.execute(f"SELECT * FROM bot_user WHERE chat_id = ?;", (chat_id,))
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO bot_user (chat_id, first_name) VALUES (?, ?);", (chat_id, first_name))
        conn.commit()
        return True
    else:
        return False

def show_users():
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bot_user')
    rows = cursor.fetchall()

    for row in rows:
        print(row)


def get_user_ids():
    conn = sqlite3.connect('memory_game.db')
    cursor = conn.cursor()

    cursor.execute("SELECT chat_id FROM bot_user")
    chat_ids = cursor.fetchall()

    return [id[0] for id in chat_ids]

