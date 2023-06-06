import sqlite3

class Database(object):
    _instance = None  # Singleton design
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        pass