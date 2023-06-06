import json
from typing import Any, Coroutine
import discord, os
from discord import app_commands
from discord.ext import commands

class GatekeeperBot(commands.Bot):
    def __init__(self)->None:
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.synced = False
        
        super().__init__(command_prefix="!", 
                         description=":^)", 
                         intents=intents,
                         application_id=1115019763647778867)
        
    async def setup_hook(self):
        await self.load_extension("cogs.minecraft")
        
    def changeSyncState(self, state: bool = False):
        self.synced = state
        
        
bot = GatekeeperBot()

@bot.event
async def on_ready():
    await bot.tree.sync()
    bot.changeSyncState(state=True)
    
    print(f"{bot.user} is ready.")
    

if __name__ == "__main__":
    with open("config.json", "r") as f:
        TOKEN = json.load(f)["token"]
    
    bot.run(token=TOKEN)
    