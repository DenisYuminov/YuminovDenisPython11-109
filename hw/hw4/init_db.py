import sqlite3

connection = sqlite3.connect('database')

cur = connection.cursor()

connection.close()