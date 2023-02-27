import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
print ("DB Conncetion opened")

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Third Post', 'Content for the third post')
            )

print ("INSERTS executed")
connection.commit()
connection.close()

print ("DB connection closed")
# Created by Bahadur Singh singh.bahadur@gmail.com
