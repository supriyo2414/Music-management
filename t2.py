import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('DROP TABLE songs')
print ("Table drop successfully")
