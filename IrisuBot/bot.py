import json
import logging
from typing import Any, Coroutine, Optional
import discord, os
from discord import app_commands
from discord.ext import commands
from discord.utils import MISSING

from database import SQLiteDatabase

EXT = ["cogs.minecraft",
        "cogs.moderation",
        "cogs.core"]


class Config(object):
    application_id : int
    owner_id : int
    token : str
    db_path : str
    
    @classmethod
    def load(cls, path: str):
        with open(path, "r") as f:
            config = json.load(f)
        cls.token = config["token"]
        cls.application_id = config["application_id"]
        cls.owner_id = config["owner_id"]
        cls.db_path = config["db_path"]
    

class IrisuBot(commands.Bot):
    def __init__(self, application_id: int, owner_id: int, db_path: str)->None:
        intents = discord.Intents.all()
        self.db : SQLiteDatabase = SQLiteDatabase(path=db_path)
        
        super().__init__(command_prefix="!", 
                         description=":^)", 
                         intents=intents,
                         application_id=application_id,
                         owner_id=owner_id)
        
    async def setup_hook(self):
        # Load cogs
        for i in range(0, len(EXT)):
            print(f"Loaded {EXT[i]}")
            await self.load_extension(EXT[i])

Config.load("./config.json")
bot = IrisuBot(application_id=Config.application_id,
               owner_id=Config.owner_id,
               db_path=Config.db_path)

@bot.event
async def on_ready():    
    await bot.change_presence(status=discord.Status.online, 
                              activity=discord.Game("MCServer offline..."))
    print(f"{bot.user} is ready.")
    

if __name__ == "__main__":
    bot.run(token=Config.token)
    