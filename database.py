import sqlite3

conn = sqlite3.connect('user.db')

conn.execute('''CREATE TABLE user(
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                PRIMARY KEY(username);
            )''')

