import pymongo


class Database(object):  # Singleton
    _instance = None  # Singleton design
    client : pymongo.MongoClient = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(cls, host : str = "127.0.0.1", port : int = 27017) -> None:
        cls.client = pymongo.MongoClient(host=host, port=port)
    
    def insert(cls):
        collection = cls.client["irisubot"]["members"]
        items = collection.find()
        print(items)