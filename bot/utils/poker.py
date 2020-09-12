import random
import discord
from bot.configs.constants import flower_emotes

flower_choices = []
class Flowers:
    def __init__(self, color):
        self.color = color
        self.emote = self.get_emote()

    def get_emote(self):
        return flower_emotes.get(self.color)


class Game:
    def __init__(self, channel):
        self.participants = {}
        self.channel = channel
        self.flowers = []
        self.pair_count = 0
        self.build()

    def build(self):
        for _ in range(1):
            for flower in flower_emotes:
                flower_choices.append(Flowers(flower))
        self.get_random_flowers(self)

    @staticmethod
    def get_pair_count(item_list: list):
        pair_count = 0
        color_list = list(item.color for item in item_list)
        for key in set(color_list):
            pair_count += color_list.count(key) // 2
        return pair_count

    def get_random_flowers(self, player):
        for _ in range(5):
            for _ in range(random.randint(1, 9)):
                random.shuffle(flower_choices)
            player.flowers.append(random.choices(flower_choices)[0])
        player.pair_count = self.get_pair_count(player.flowers)


class Player:
    message: discord.Message

    def __init__(self, user_id, bet_amount, game):
        self.id = user_id
        self.bet_amount = bet_amount
        self.game = game
        self.flowers = []
        self.planted = False
        self.pair_count = 0
