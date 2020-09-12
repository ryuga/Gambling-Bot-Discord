import discord
from discord.ext import commands
from bot.utils.poker import Game, Player
from bot.configs.constants import FLOWERPOKER_MAX_PLAYERS, flower_poker_emoji_id
from bot.utils.embed_handler import simple_embed, fp_embed


class Jack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.live_games = {}
        self.reactable_messages = {}
        self._reaction_options = {
            flower_poker_emoji_id: self.plant
        }

    async def plant(self, player):
        me = self.bot.get_user(player.id)
        await player.message.edit(embed=fp_embed(me, player))

    async def init_flower_poker(self, ctx, bet_amount):
        if ctx.channel.id in self.live_games:
            game = self.live_games[ctx.channel.id]
        else:
            game = Game(ctx.channel.id)
            self.live_games[ctx.channel.id] = game

        if not len(self.live_games) == FLOWERPOKER_MAX_PLAYERS:
            player = Player(ctx.author.id, bet_amount, game)
            if ctx.author.id not in game.participants:
                game.participants[ctx.author.id] = player
                player.game.get_random_flowers(player)
                msg = await ctx.channel.send(embed=fp_embed(ctx.author, player, hidden=True))
                player.message = msg
                self.reactable_messages[msg.id] = player
                reaction = self.bot.get_emoji(flower_poker_emoji_id)
                await msg.add_reaction(reaction)
            else:
                await ctx.channel.send(embed=simple_embed("", "You've already joined the game."
                                                          " You can try joining another lobby."))
        else:
            await ctx.channel.send(embed=simple_embed("", "The lobby if full. Try in another channel."))

    @commands.command()
    async def f(self, ctx, bet_amount):
        await self.init_flower_poker(ctx, bet_amount)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in self.reactable_messages:
            player = self.reactable_messages.get(payload.message_id)
            try:
                if payload.user_id == player.id:
                    await self._reaction_options[payload.emoji.id](player)  # noqa
            except Exception as E:
                print("Exception:", E)


def setup(bot):
    bot.add_cog(Jack(bot))
