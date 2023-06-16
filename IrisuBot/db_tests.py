import database

db = database.SQLite(path="./database.db")
db2 = db = database.SQLite()

print(id(db) == id(db2))