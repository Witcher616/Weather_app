from .Base import connect_db, commit_and_close


def check_user_exists(db_name, user_name):
    conn, cursor = connect_db(db_name)
    cursor.execute('SELECT * FROM users where user_name = ?;', (user_name,))
    user = cursor.fetchone()
    if not user:
        return False, False
    return True, user[0]


def add_user(db_name, user_name):
    conn, cursor = connect_db(db_name)
    cursor.execute('INSERT INTO users(user_name) VALUES (?)', (user_name,))
    commit_and_close(conn)
    print('user added:', user_name)


def add_weather(db_name, **kwargs):
    conn, cursor = connect_db(db_name)
    keys = ', '.join(list(kwargs.keys()))
    values = tuple(kwargs.values())
    signs = ', '.join(['?' for _ in range(len(values))])
    sql = f"INSERT INTO weather({keys}) Values({signs})"
    cursor.execute(sql, values)
    commit_and_close(conn)


def get_user_weather(db_name, user_id):
    conn, cursor = connect_db(db_name)
    sql = "SELECT * FROM weather WHERE user_id = ?;"
    cursor.execute(sql, (user_id,))
    return cursor.fetchall()


def clear_user_weather(db_name, user_id):
    conn, cursor = connect_db(db_name)
    sql = "DELETE FROM weather WHERE user_id = ?;"
    cursor.execute(sql, (user_id, ))
    commit_and_close(conn)
