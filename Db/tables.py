from Db.Base import connect_db, commit_and_close


def create_users_table():
    conn, cursor = connect_db("../weather.db")

    sql = """
        DROP TABLE IF EXISTS users;
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT
        );
    """

    cursor.executescript(sql)

    commit_and_close(conn)


def create_weather_table():
    conn, cursor = connect_db("../weather.db")
    sql = """
        Drop TABLE IF Exists weather;
        Create TABLE IF NOT EXISTS weather(
            weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            tz INTEGER,
            sunrise DATETIME,
            sunset DATETIME,
            dt DATETIME,
            description TEXT,
            speed DECIMAL,
            temp DECIMAL,
            user_id INTEGER REFERENCES users(user_id)
        );
    """
    cursor.executescript(sql)

# create_users_table()
# create_weather_table()
