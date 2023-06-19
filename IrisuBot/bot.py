import json
from typing import Any, Coroutine
import discord, os
from discord import app_commands
from discord.ext import commands

from database import SQLiteDatabase

EXT = ["cogs.minecraft",
        "cogs.moderation",
        "cogs.basic"]

class GatekeeperBot(commands.Bot):
    def __init__(self, app_id:int)->None:
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.synced = False
        self.db = SQLiteDatabase("./database.db");
        
        super().__init__(command_prefix="!", 
                         description=":^)", 
                         intents=intents,
                         application_id=app_id,
                         owner_id=975512354265636874)
        
    async def setup_hook(self):
        
        self.db = SQLiteDatabase("./database.db")
        
        # Load cogs
        for i in range(0, len(EXT)):
            print(f"Loaded cogs.{EXT[i]}")
            await self.load_extension(EXT[i])
        
    def changeSyncState(self, state: bool = False):
        self.synced = state
        
with open("./config.json", "r") as f:
    config = json.load(f)
    TOKEN = config["token"]
    APP_ID = config["application_id"]

bot = GatekeeperBot(app_id=APP_ID)

@bot.event
async def on_ready():
    bot.changeSyncState(state=True)
    
    await bot.change_presence(status=discord.Status.online, 
                              activity=discord.Game("MCServer offline..."))
    
    print(f"{bot.user} is ready.")
    

if __name__ == "__main__":
    bot.run(token=TOKEN)
    