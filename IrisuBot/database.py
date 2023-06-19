import os
import sqlite3
from typing import Any

import discord
import pymongo
import pymongo.errors
from mojang import MojangAPI
from patterns import Singleton

TABLES = [
    "members"
]
        
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
    def database_query(func):
        def wrapper(self):
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
    
    @database_query
    def checkMemberIsAdmin(self, id: int):
        stmt = f"SELECT id FROM members WHERE member_id={id} AND member_admin=1"
        self.cursor.execute(stmt)
        

class MongoDB(object, metaclass=Singleton):
    '''i have no idea how pymongo works - it's not giving any expections lmaoooo'''
    
    MEMBER_TEMPLATE :dict = {
        "_id": None,                ## id - discord id
        "discord_name": None,       ## str
        "minecraft_name": None,     ## str
        "minecraft_uuid": None,     ## str
        "is_admin": None,           ## bool
    }
    
    BOT_TEMPLATE : dict = {
        "_id": None,
        "command_prefix": "!",
        "admin_role": None,
        "relay_channel": None,
        "bot_channel": None
    }
    
    def __init__(self, db : str = "irisubot") -> None:
        self.client = pymongo.MongoClient(host="0.0.0.0", port=900)
        
        try: self.client.admin.command('ping')
        except Exception as e:
            print("")
        else:
            pass
        
        
    def getDatabase(self):
        pass
            
    def addMember(self):
        pass


class StatementBuilder(object):
    
    @staticmethod
    def insert(table: str, **items) -> str:
        ## me when list comprehension
        keys = ",".join(["`" + key+ "`" for key in items.keys()])
        values = ",".join(["'" + str(value) + "'" if isinstance(value, str) else str(value) for value in items.values()])
        
        return f"INSERT INTO {table} ({keys}) VALUES ({values})"