import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE songs (sond_id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT, artist TEXT, album TEXT ,song_name TEXT,song BLOB)')
print ("Table created successfully")
conn.close()
