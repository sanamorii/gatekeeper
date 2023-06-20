import os
import sqlite3

# import pymongo
# import pymongo.errors


from typing import Any, Literal, Union, Optional, Tuple
from discord import User, Member, Guild, Interaction
from discord.ext.commands import Context
from patterns import Singleton

class SQLiteDatabase(object, metaclass=Singleton):

    def __init__(self, path: str = ":memory:") -> None:
        self.path : str = path
        self.conn : sqlite3.Connection = sqlite3.connect(path)
        self.cursor : sqlite3.Cursor = self.conn.cursor()  ## created via context manager
        
        self.tables = [
            "users",
            "members",
            "guilds"
        ]
        
        self._initialisation()
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()
        
        
    def _initialisation(self):
        print("Database connected.")

        stmt = """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}';"""
        for table in self.tables:
            self.cursor.execute(stmt.format(table))
            if self.cursor.fetchone()[0] != 1:
                print(f"SQLite3: Table irisu.{table} does not exist. -> Creating...")
            else:
                print(f"SQLite3: Table irisu.{table} exists.")
        
    def addUser(self, user : Union[User, Member]) -> None:
        stmt = """INSERT INTO users (`user_id`,`user_name`,`user_type`) VALUES (?,?,?);"""
        type = "bot" if user.bot else "user"
        
        self.cursor.execute(stmt, (user.id, user.name, type,))
        self.conn.commit()
    
    def userExists(self, user : Union[User, Member]) -> bool:
        stmt = "SELECT count(*) FROM users WHERE user_id=?"
        self.cursor.execute(stmt, (user.id,))
        if self.cursor.fetchone()[0] < 1:
            return False
        return True
    
    def linkUser(self, user: Union[User, Member], mc_data: dict) -> None:
        stmt = """UPDATE users SET user_mcname = ?, user_mcuuid = ?, user_linked = ? WHERE user_id = ?"""
        self.cursor.execute(stmt, (mc_data["name"], mc_data["id"], 1, user.id,))
        self.conn.commit()
        
    def updateLinkedAccount(self, user: Union[User, Member], mc_data: dict) -> bool:
        sel_stmt = """SELECT user_mcname, user_mcuuid FROM users WHERE user_id = ?;"""
        upd_stmt = """UPDATE users SET {} = ? WHERE user_id = ?;"""
        self.cursor.execute(sel_stmt, (user.id,))
        data = self.cursor.fetchone()
        
        if data[0] != mc_data["name"]:  ## only changing the name 
            self.cursor.execute(upd_stmt.format("user_mcname"), (mc_data["name"], user.id, ))

        if data[1] != mc_data["id"]:
            self.cursor.execute(upd_stmt.format("user_mcuuid"), (mc_data["id"], user.id, ))
            return True
        return False            
        
        
    def isUserLinked(self, user: Union[User, Member]) -> None:
        stmt = """SELECT user_linked FROM users WHERE user_id=?;"""
        self.cursor.execute(stmt, (user.id,))
        if self.cursor.fetchone()[0] < 1:  ## not linked
            return False
        return True
    
    def addMember(self, member: Union[User, Member], guild: Guild) -> None:
        stmt = """INSERT INTO members (`user_id`, `guild_id`, `member_nickname`) VALUES (?,?,?)"""
        self.cursor.execute(stmt, (member.id, guild.id, member.nick,))
        self.conn.commit()
    
    def memberExists(self, member : Union[User, Member], guild: Guild) -> bool:
        stmt = "SELECT count(*) FROM members WHERE user_id=? AND guild_id=?;"
        self.cursor.execute(stmt, (member.id, guild.id))
        if self.cursor.fetchone()[0] < 1:
            return False
        return True
    
    
    def guildExists(self, guild: Guild) -> bool:
        stmt = """SELECT count(*) FROM guilds WHERE guild_id=?"""
        self.cursor.execute(stmt, (guild.id,))
        if self.cursor.fetchone()[0] < 1:
            return False
        return True
        
    
    def addGuild(self, guild: Guild) -> int:
        """Add `guild` into database

        Args:
            guild (Guild): guild object to add
        """
        
        stmt = """INSERT INTO guilds (`guild_id`, `guild_name`) VALUES (?, ?);"""
        self.cursor.execute(stmt, (guild.id, guild.name))
        self.conn.commit()
        
        for count, member in enumerate(guild.members, start=1):
            if not self.userExists(user=member):
                self.addUser(user=member)
            if not self.memberExists(member=member, guild=guild):
                self.addMember(member=member, guild=guild)

        return count
    
    def updateGuild(self, guild: Guild) -> bool:
        """Update guild entry in database

        Args:
            guild (Guild): guild object to update

        Returns:
            bool: returns `True` on update. `False` if guild entry is up-to-date.
        """
        stmt = """SELECT * FROM guilds WHERE guild_id = ?;"""
        self.cursor.execute(stmt, (guild.id,))
        guildData = self.cursor.fetchone()
    
    def setGuildHost(self, guild: Guild, type: Literal["host", "rcon"], **data):
        stmt = """UPDATE guilds SET {} = ?, {} = ? WHERE guild_id = ?;"""        
        match type:
            case "host":
                self.cursor.execute(stmt.format("guild_hostip", "guild_hostport"),
                                    (data["host_ip"], data["host_port"], guild.id,))
            case "rcon":
                self.cursor.execute(stmt.format("guild_rconpass", "guild_rconport"),
                                    (data["rcon_pass"], data["rcon_port"], guild.id,))
            case _:
                raise Exception("wtf did you do???")
        self.conn.commit()
    
    ## sqlite does not support arrays
    @staticmethod
    def encode(arr: list): return ",".join(arr)
    
    @staticmethod
    def decode(string: str): return string.split(",")
        

# class MongoDB(object, metaclass=Singleton):
#     '''i have no idea how pymongo works - it's not giving any expections lmaoooo'''
    
#     MEMBER_TEMPLATE :dict = {
#         "_id": None,                ## id - discord id
#         "discord_name": None,       ## str
#         "minecraft_name": None,     ## str
#         "minecraft_uuid": None,     ## str
#         "is_admin": None,           ## bool
#     }
    
#     BOT_TEMPLATE : dict = {
#         "_id": None,
#         "command_prefix": "!",
#         "admin_role": None,
#         "relay_channel": None,
#         "bot_channel": None
#     }
    
#     def __init__(self, db : str = "irisubot") -> None:
#         self.client = pymongo.MongoClient(host="0.0.0.0", port=900)
        
#         try: self.client.admin.command('ping')
#         except Exception as e:
#             print("")
#         else:
#             pass
        
        
#     def getDatabase(self):
#         pass
            
#     def addMember(self):
#         pass