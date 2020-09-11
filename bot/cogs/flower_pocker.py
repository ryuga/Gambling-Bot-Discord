import discord
from discord.ext import commands


class Jack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def f(self, ctx, bet_amount):
        pass


def setup(bot):
    bot.add_cog(Jack(bot))
