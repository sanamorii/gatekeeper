import json
from typing import Any, Coroutine
import discord, os
from discord import app_commands
from discord.ext import commands

from database import SQLiteDatabase

EXT = ["cogs.minecraft",
        "cogs.moderation"]

class GatekeeperBot(commands.Bot):
    def __init__(self)->None:
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.synced = False
        self.db = None;
        
        super().__init__(command_prefix="!", 
                         description=":^)", 
                         intents=intents,
                         application_id=1115019763647778867)
        
    async def setup_hook(self):
        
        self.db = SQLiteDatabase("./database.db")
        
        # Load cogs
        for i in range(0, len(EXT)):
            print(f"Loaded cogs.{EXT[i]}")
            await self.load_extension(EXT[i])
        
    def changeSyncState(self, state: bool = False):
        self.synced = state
        
bot = GatekeeperBot()

@bot.event
async def on_ready():
    await bot.tree.sync()
    bot.changeSyncState(state=True)
    
    await bot.change_presence(status=discord.Status.online, 
                              activity=discord.Game("MCServer offline..."))
    
    print(f"{bot.user} is ready.")
    

if __name__ == "__main__":
    with open("./config.json", "r") as f:
        TOKEN = json.load(f)["token"]

    bot.run(token=TOKEN)
    