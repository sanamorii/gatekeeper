import discord
from discord.ext import commands
from discord import app_commands
from exceptions import InvalidMinecraftUsername

class Moderation(commands.Cog, group_name="MinecraftIntegration"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="test")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong", ephemeral=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))