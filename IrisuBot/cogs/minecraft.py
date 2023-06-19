import asyncio
import discord
import exceptions
from discord.ext import commands
from discord import app_commands
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
                await client.whitelistAdd(username)
                
        except exceptions.PlayerDoesNotExist as e:
            msg = f"Invalid minecraft username."
        except exceptions.PlayerAlreadyExists as e:
            
            ## In the case where the player has been whitelisted but 
            ## not added to the database.
            if not self.bot.db.isMember(member=user):
                self.bot.db.addMember(member=user, mc_data=content)
                msg = f"{username} already exists in the whitelist.\n{user.name} has been registered."
            else:
                msg = f"{username} has already been registered."
            
        else:
            self.bot.db.addMember(member=user, mc_data=content)
            msg = f"{user.name} -> {username} has been registered"
        await interaction.response.send_message(msg, ephemeral=True)
        
        
    
    ## chat relay
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     print(f"{message.content}")

async def setup(bot: commands.Bot):
    await bot.add_cog(MinecraftIntegration(bot))