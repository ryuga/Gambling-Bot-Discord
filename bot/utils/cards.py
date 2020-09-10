import random

import discord
from bot.configs.constants import red_emotes, black_emotes


class Card(object):
    def __init__(self, suit, name):
        self.suit = suit
        self.name = name
        self.emote = self._get_emoji()

    def show(self):
        print(f"{self.name} of {self.suit}")

    def _get_emoji(self):
        if self.suit in ["Diamond", "Heart"]:
            return red_emotes.get(self.name)
        else:
            return black_emotes.get(self.name)


class Deck:
    def __init__(self):
        self.cards = []
        self.build_deck()
        self.shuffle()

    def build_deck(self):
        suits = ["Club", "Heart", "Diamond", "Spade"]
        cards_set = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "K", "Q", "J"]
        for suit in suits:
            for card in cards_set:
                self.cards.append(Card(suit, card))

    def show(self):
        for card in self.cards:
            card.show()

    def shuffle(self):
        for _ in range(random.randint(1, 9)):
            random.shuffle(self.cards)

    def get_random_cards(self, count):
        cards_list = []
        for i in range(count):
            random_card = random.choice(self.cards)
            cards_list.append(random_card)
            self.cards.remove(random_card)
        return cards_list

    def give_random_card(self, player, count):
        for random_card in self.get_random_cards(count):
            player.cards_owned.append(random_card)


class Game:
    def __init__(self, channel):
        self.channel = channel
        self.participants = {}
        self.deck = Deck()
        self.dealer_cards = self.deck.get_random_cards(2)


class Player:
    message: discord.Message

    def __init__(self, user_id, bet_amount, game):
        self.user_id = user_id
        self.bet_amount = bet_amount
        self.card_value = 0
        self.cards_owned = []
        self.game = game
        self.stay = False
