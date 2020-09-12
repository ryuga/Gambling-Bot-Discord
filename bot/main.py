import discord
from discord.ext import commands
from bot.configs.secrets import TOKEN

bot = commands.Bot(command_prefix=('!',))
game = discord.Game(name='Securing the server')


def setup():
    bot.run(TOKEN)


@bot.event
async def on_ready():
    # bot.load_extension("cogs.blackjack")
    bot.load_extension("cogs.flower_poker")
    print('ready')


@bot.event
async def on_command_error(ctx, error):  # noqa
    await ctx.send(error)

setup()
