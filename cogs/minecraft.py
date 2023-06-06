import discord
from discord.ext import commands
from discord import app_commands

from connection.mojang import MojangAPI


class MinecraftIntegration(commands.Cog, group_name="MinecraftIntegration"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="test")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong", ephemeral=False)

    @app_commands.command(name="add", description="Add your username to the whitelist.")
    @app_commands.describe(username="Your Minecraft username")
    async def whitelist_add(self, interaction: discord.Interaction, username:str):
        MojangAPI.usernameToUUID(username)
        await interaction.response.send_message(f"DEBUG: {username}", ephemeral=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(MinecraftIntegration(bot))