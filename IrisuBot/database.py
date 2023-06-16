import os
import sqlite3
from typing import Any

import discord
import pymongo
from mojang import MojangAPI

TABLES = [
    "members"
]

class Singleton(type):  # Singleton
    _instances = {} # Singleton design    
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

        
class SQLiteDatabase(object, metaclass=Singleton):

    def __init__(self, path: str = ":memory:") -> None:
        self.path : str = path
        self.conn : sqlite3.Connection = None
        self.cursor : sqlite3.Cursor = None  ## created via context manager
        
        self._initialisation()
        
    def _initialisation(self):
        print("Database connected.")

    
    def __enter__(self, *args, **kwargs):

        return self
    
    def __exit__(self, *args, **kwargs):
        self.conn.commit()
        

    ## stupid decorator thingy
    def database_query(self, func):
        def wrapper():
            self.conn = sqlite3.connect(self.path)
            self.cursor = self.conn.cursor()
            func()
            self.cursor.close()
            self.conn.close()
        return wrapper
    
    
    def _checkTables(self):
        pass
    
    @database_query
    def addMember(self, member: discord.User, content: dict):
        
        ## Build insert SQL statement
        stmt = StatementBuilder.insert(table="members",
                                member_id=member.id,
                                member_nickname=member.display_name,
                                member_dcname=member.name,
                                member_mcname=content["name"],
                                member_mcuuid=content["id"]
                            )
        self.cursor.execute(stmt)
    
    def get(self, table: str, key: str, value: Any):
        pass
    
class StatementBuilder(object):
    
    @staticmethod
    def insert(table: str, **items) -> str:
        keys = ",".join(["`" + key+ "`" for key in items.keys()])
        values = ",".join(["'" + str(value) + "'" if isinstance(value, str) else str(value) for value in items.values()])
        
        return f"INSERT INTO {table} ({keys}) VALUES ({values})"

    @staticmethod 