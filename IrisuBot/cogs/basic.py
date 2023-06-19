import discord
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name="sync")
    async def sync_commands(self, ctx)