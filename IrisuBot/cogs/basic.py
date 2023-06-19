import discord
from discord.ext import commands
from discord.ext.commands import Context

class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name="sync")
    @commands.is_owner()
    @commands.guild_only()
    async def sync_commands(self, ctx: Context):
        try:
            await ctx.bot.tree.sync(guild=ctx.guild)
        except Exception as e:
            await ctx.send(f"fatal error {e.with_traceback()}")
        else:
            await ctx.send(f"Commands synced")


async def setup(bot: commands.Bot):
    await bot.add_cog(Basic(bot))