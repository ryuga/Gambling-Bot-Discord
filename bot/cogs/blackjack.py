import discord
from discord.ext import commands

from bot.utils.cards import Game, Player
from bot.utils.embed_handler import simple_embed, jack_embed, bj_bust_embed, bj_win_embed, bj_push_embed
from bot.configs.constants import hit_emote_id, stay_emote_id, double_emote_id

face_cards = ["K", "Q", "J"]
MAX_PLAYERS = 4


class Jack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.live_games = {}
        self.reactable_messages = {}
        self._reaction_options = {
            hit_emote_id: self.hit,
            stay_emote_id: self.stay,
            double_emote_id: self.double
        }

    @staticmethod
    async def calculate_card_value(cards: list, dealer=False):
        value = 0
        a_count = 0
        for card in cards:
            if card.name == "A":
                a_count += 1
            elif card.name in face_cards:
                value += 10
            else:
                value += int(card.name)
        if not dealer:
            if a_count != 0:
                for _ in range(a_count):
                    if value + 11 > 21:
                        value += 1
                    else:
                        value += 11
            return value
        else:
            if a_count != 0:
                for _ in range(a_count):
                    if value > 17:
                        value += 1
                    else:
                        value += 11
            return value

    async def check_blackjack(self, player):
        player.card_value = await self.calculate_card_value(player.cards_owned)
        if player.card_value > 21:
            await self.bust(player)
        if player.card_value == 21:
            await self.blackjack(player)

    async def evaluate_results(self, game):
        participants = game.participants
        dealer_card_value = await self.calculate_card_value(game.dealer_cards)
        for player in list(participants):
            if dealer_card_value > 21:
                await self.win_blackjack(participants[player])
            elif dealer_card_value > participants[player].card_value:
                await self.lose_blackjack(participants[player])
            elif dealer_card_value < participants[player].card_value:
                await self.win_blackjack(participants[player])
            else:
                await self.push_blackjack(participants[player])

    async def win_blackjack(self, player):
        me = self.bot.get_user(player.user_id)
        await player.message.edit(embed=bj_win_embed(me, player, show=True))
        await self.remove(player)

    async def lose_blackjack(self, player):
        me = self.bot.get_user(player.user_id)
        await player.message.edit(embed=bj_bust_embed(me, player, show=True))
        await self.remove(player)

    async def push_blackjack(self, player):
        me = self.bot.get_user(player.user_id)
        await player.message.edit(embed=bj_push_embed(me, player))
        await self.remove(player)

    async def dealers_play(self, game):
        print("Dealer plays")
        while True:
            cards = game.dealer_cards
            card_value = await self.calculate_card_value(cards, dealer=True)
            if card_value < 17:
                random_cards = game.deck.get_random_cards(1)
                game.dealer_cards.append(random_cards[0])
            else:
                break
        await self.evaluate_results(game)

    async def remove(self, player):
        await player.message.clear_reactions()
        player.game.participants.pop(player.user_id)
        self.reactable_messages.pop(player.message.id)
        del player

    async def blackjack(self, player):
        me = self.bot.get_user(player.user_id)
        embed = bj_win_embed(me, player, show=True)
        embed.title = "BlackJack!"
        if await self.calculate_card_value(player.game.dealer_cards) == 21:
            await self.push_blackjack(player)
        else:
            await player.message.edit(embed=embed)
        await self.remove(player)

    async def bust(self, player):
        me = self.bot.get_user(player.user_id)
        embed = bj_bust_embed(me, player)
        embed.title = "Busted!"
        await player.message.edit(embed=embed)
        await self.remove(player)

    async def hit(self, player):
        player.game.deck.give_random_card(player, 1)
        me = self.bot.get_user(player.user_id)
        await player.message.edit(embed=jack_embed(me, player))
        await self.check_blackjack(player)
        await self.check_active_session(player.game)

    async def check_active_session(self, game):
        active_game_session = False
        participants = game.participants
        for person in participants:
            if participants[person].stay is False:
                active_game_session = True
        if not active_game_session:
            await self.dealers_play(game)

    async def stay(self, player):
        player.stay = True
        await self.check_blackjack(player)
        me = self.bot.get_user(player.user_id)
        await player.message.clear_reactions()
        embed = jack_embed(me, player)
        embed.description = f"**Your bet: ** {player.bet_amount}\n"\
                            f"**Status: **Waiting for other players..."
        await player.message.edit(embed=embed)
        await self.check_active_session(player.game)

    async def double(self, player):
        # debit twice the amount
        player.bet_amount *= 2
        player.game.deck.give_random_card(player, 1)
        me = self.bot.get_user(player.user_id)
        await player.message.edit(embed=jack_embed(me, player))
        await self.stay(player)

    async def init_blackjack(self, ctx, bet_amount):
        if ctx.channel.id in self.live_games:
            game = self.live_games[ctx.channel.id]
        else:
            game = Game(ctx.channel.id)
            self.live_games[ctx.channel.id] = game

        if not len(game.participants) == 4:
            player = Player(ctx.author.id, bet_amount, game)
            if ctx.author.id not in game.participants:
                game.participants[ctx.author.id] = player
                game.deck.give_random_card(player, 2)
                embed = jack_embed(ctx.author, player)
                msg = await ctx.channel.send(embed=embed)
                player.message = msg
                self.reactable_messages[msg.id] = player
                emotes = [hit_emote_id, stay_emote_id, double_emote_id]
                for emote in emotes:
                    reaction = self.bot.get_emoji(emote)
                    await msg.add_reaction(reaction)
                await self.check_blackjack(player)
            else:
                await ctx.channel.send(embed=simple_embed("You've already joined the game."
                                                          " You can try joining another lobby."))
        else:
            await ctx.channel.send(embed=simple_embed("The lobby if full. Try in another channel."))

    @commands.command()
    async def b(self, ctx, bet_amount):
        await self.init_blackjack(ctx, bet_amount)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in self.reactable_messages:
            reaction = self.bot.get_emoji(payload.emoji.id)
            user = self.bot.get_user(payload.user_id)
            player = self.reactable_messages.get(payload.message_id)
            if user is not self.bot.user:
                await player.message.remove_reaction(reaction, user)
            try:
                if payload.user_id == player.user_id:
                    await self._reaction_options[payload.emoji.id](player)  # noqa
            except Exception as E:
                print(E)


def setup(bot):
    bot.add_cog(Jack(bot))
