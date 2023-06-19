import pymongo

client = pymongo.MongoClient("127.0.0.1")
hello = client["hhhhhh"]

hello.list_collection_names()