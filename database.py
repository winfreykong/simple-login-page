import sqlite3

conn = sqlite3.connect('user.db')

cursor = conn.cursor()

# Check if table exists
cursor.execute(''' SELECT name FROM sqlite_master WHERE type='table' AND name='user' ''')

# Clear table if exists
if cursor.fetchone()[0]==1:
    print('Table exists. Clearing table now..')
    cursor.execute('DELETE FROM students;',)

# Create table if does not exist
else:
    conn.execute('''CREATE TABLE user(
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                PRIMARY KEY(username)
            );''')
conn.commit()
conn.close()
