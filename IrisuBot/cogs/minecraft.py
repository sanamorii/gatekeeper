import asyncio
import discord
import mojang
import exceptions

from aiomcrcon import RCONConnectionError

from discord.ext import commands
from discord import app_commands
from discord import User, Member
from integration.rcon import RCONClient
from bot import IrisuBot

class MinecraftIntegration(commands.Cog):
    def __init__(self, bot: IrisuBot) -> None:
        self.bot : IrisuBot = bot

    @app_commands.command(name="register", description="Add your account to the whitelist.")
    @app_commands.describe(username="Your Minecraft username")
    async def register(self, interaction: discord.Interaction, username:str):
        
        try:
            content = mojang.usernameToUUID(username)
            async with RCONClient() as client:
                await client.whitelistAdd(username)
                
        except exceptions.PlayerDoesNotExist:
            msg = f"Minecraft account `{username}` is invalid."
        except exceptions.AlreadyWhitelisted:
            msg = f"Minecraft account `{username}` is already whitelisted."
        except RCONConnectionError:
            await interaction.response.send_message("**cannot connect to server rcon** - please contact the developer thanks :thumbs_up:")
            return
        else:
            msg = f"Minecraft account `{username}` has been whitelisted."
            
        ## check if user exists in user or member tables
        if not self.bot.db.userExists(user=interaction.user):
            self.bot.db.addUser(user=interaction.user)
            
        if not self.bot.db.memberExists(member=interaction.user, guild=interaction.guild):
            self.bot.db.addMember(member=interaction.user, guild=interaction.guild)
        
        ## check if user has mc account linked
        if not self.bot.db.isUserLinked(user=interaction.user):
            self.bot.db.linkUser(user=interaction.user, mc_data=content)
            msg += "\nYour discord account has been linked to your Minecraft Account."

        elif self.bot.db.updateLinkedAccount(user=interaction.user, mc_data=content):
            msg += "\nYour discord account has been linked to your Minecraft Account."
            
        await interaction.response.send_message(msg, ephemeral=True)
        
    ## chat relay
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     print(f"{message.content}")

@app_commands.guild_only()
class SetInfo(commands.GroupCog, name="set", description="Set server information"):
    def __init__(self, bot: IrisuBot) -> None:
        self.bot = bot
        super().__init__()
    
    @app_commands.command(name="server")
    @app_commands.describe(host="Minecraft server IP address (required)", 
                           port="Minecraft server port (defaults to 25565)")
    async def server(self, interaction: discord.Interaction, host:str, port:int = 25565) -> None:
        try:
            self.bot.db.setGuildHost(guild=interaction.guild, type="host", host_ip=host, host_port=port)
        except Exception as e:
            await interaction.response.send_message(f"Failed to set host info -> {e}", ephemeral=True)
        else:
            await interaction.response.send_message("Server host info set.", ephemeral=True)

    @app_commands.command(name="rcon")
    @app_commands.describe(passwd="Minecraft rcon password (defaults to None)", 
                           port="Minecraft rcon port (defaults to 25565)")
    async def rcon(self, interaction: discord.Interaction, passwd:str = None, port:int = 25575) -> None:
        try:
            self.bot.db.setGuildHost(guild=interaction.guild, type="rcon", rcon_pass=passwd, rcon_port=port)
        except Exception as e:
            await interaction.response.send_message(f"Failed to set rcon info -> {e}", ephemeral=True)
        else:
            await interaction.response.send_message("Server rcon info set.", ephemeral=True)
            

async def setup(bot: IrisuBot):
    await bot.add_cog(MinecraftIntegration(bot))
    await bot.add_cog(SetInfo(bot))