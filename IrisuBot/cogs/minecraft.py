import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from exceptions import InvalidMinecraftUsername
from integration.rcon import RCONClient

from mojang import MojangAPI
from database import SQLiteDatabase

class MinecraftIntegration(commands.Cog, group_name="MinecraftIntegration"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.server = RCONClient()

    @app_commands.command(name="register", description="Add your account to the whitelist.")
    @app_commands.describe(username="Your Minecraft username")
    async def register(self, interaction: discord.Interaction, username:str):
        user = interaction.user
        
        try:
            content = MojangAPI.usernameToUUID(username)
            async with RCONClient() as client:
                await client.whitelistAdd()
        except InvalidMinecraftUsername as e:
            msg = f"Invalid minecraft username"
        else:
            self.bot.db.addMember()
            msg = "Account added to the whitelist."
        await interaction.response.send_message(msg, ephemeral=False)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"{message.content}")

async def setup(bot: commands.Bot):
    await bot.add_cog(MinecraftIntegration(bot))