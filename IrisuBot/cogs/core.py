import discord
import bot
from discord.ext import commands
from discord.ext.commands import Context
from typing import Literal, Optional

class Core(commands.Cog):
    def __init__(self, bot: bot.IrisuBot) -> None:
        self.bot = bot
    
    @commands.command(name="sync")
    @commands.is_owner()
    @commands.guild_only()
    async def sync_commands(self, ctx: Context, opt: Optional[Literal["commands", "guild"]]):
        match opt:
            case "commands":
                try: await ctx.bot.tree.sync(guild=ctx.guild)
                except Exception as e: await ctx.send(f"fatal error {e.with_traceback()}")
                else: await ctx.send(f"Commands for guild `{ctx.guild.name} have been synced.")
            
            case "guild":
                log = ""
                if not self.bot.db.guildExists(guild=ctx.guild):
                    log += f"Guild doesn't exist -> Creating guild entry for {ctx.guild.name}\n"
                    self.bot.db.addGuild(guild=ctx.guild)
                else:
                    await ctx.send(f"Guild `{ctx.guild.name}` is already in the database.")
            
            case None:
                await ctx.send(f"Invalid option - avaliable options are: `commands`, `guild`")
            
            case _:  ## default case
                await ctx.send(f"Invalid option `{opt}`")
    
    # @commands.Cog.listener()
    # async def on_guild_join(self, guild: discord.Guild):
    #     guild.


async def IrisuCore(bot: bot.IrisuBot):
    await bot.add_cog(IrisuCore(bot))