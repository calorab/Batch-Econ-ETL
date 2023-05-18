import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as err:
        print(f"The error '{err}' occurred")

    return connection

connection = create_connection("/Users/AllHeart/sqlite_database")