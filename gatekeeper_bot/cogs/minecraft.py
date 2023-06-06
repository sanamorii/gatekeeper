import discord
from discord.ext import commands
from discord import app_commands
from exceptions import InvalidMinecraftUsername

from mojang import MojangAPI

class MinecraftIntegration(commands.Cog, group_name="MinecraftIntegration"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="whitelist", description="Add your account to the whitelist.")
    @app_commands.describe(username="Your Minecraft username")
    async def whitelist_add(self, interaction: discord.Interaction, username:str):
        try:
            content = MojangAPI.usernameToUUID(username)
        except InvalidMinecraftUsername as e:
            msg = f"Invalid minecraft username"
        else:
            msg = f"{content['name']} - `{content['id']}` found."
        await interaction.response.send_message(msg, ephemeral=False)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"{message.content}")

async def setup(bot: commands.Bot):
    await bot.add_cog(MinecraftIntegration(bot))