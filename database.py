import sqlite3

conn = sqlite3.connect('user.db')

conn.execute('''DROP TABLE IF EXISTS user;''')

conn.execute('''CREATE TABLE user(
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                PRIMARY KEY(username)
            );''')
conn.commit()
conn.close()
