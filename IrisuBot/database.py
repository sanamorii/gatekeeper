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
        self.conn : sqlite3.Connection = sqlite3.connect(path)
        self.cursor : sqlite3.Cursor = self.conn.cursor()  ## created via context manager
        
        self._initialisation()
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()
        
        
    def _initialisation(self):
        print("Database connected.")
    
    def addMember(self, member: discord.User, mc_data: dict):
        
        ## Build insert SQL statement
        stmt = StatementBuilder.insert(table="members",
                                member_id=member.id,
                                member_nickname=member.display_name,
                                member_dcname=member.name,
                                member_mcname=mc_data["name"],
                                member_mcuuid=mc_data["id"]
                            )
        self.cursor.execute(stmt)
    
    def isMember(self, member: discord.User) -> bool:
        stmt = """SELECT count(*) FROM members WHERE member_id=?"""
        self.cursor.execute(stmt, (member.id,))
        if self.cursor.fetchone()[0] < 1:
            return False 
        else:
            return True
    
    ## sqlite does not support arrays
    @staticmethod
    def encode(arr: list): return ",".join(arr)
    
    @staticmethod
    def decode(string: str): return string.split(",")
        

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