import random
import discord
from bot.configs.constants import flower_emotes


class Flowers:
    def __init__(self, color):
        self.color = color
        self.emote = self.get_emote()

    def get_emote(self):
        return flower_emotes.get(self.color)


class Game:
    def __init__(self, channel):
        self.flower_choices = []
        self.participants = {}
        self.channel = channel
        self.flowers = []
        self.build()

    def build(self):
        for flower in flower_emotes:
            self.flower_choices.append(Flowers(flower))
        self.get_random_flowers(self)

    def get_random_flowers(self, player):
        for _ in range(5):
            player.flowers.append(random.choices(self.flower_choices)[0])


class Player:
    message: discord.Message

    def __init__(self, user_id, bet_amount, game):
        self.id = user_id
        self.bet_amount = bet_amount
        self.game = game
        self.flowers = []
