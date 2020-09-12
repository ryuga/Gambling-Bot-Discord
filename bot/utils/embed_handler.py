import discord  # noqa
from discord import Embed  # noqa
from bot.utils.misc import get_flower_string


def simple_embed(title, desc, color=discord.Color.blue()):
    return Embed(title=title, description=desc, color=color)


def authored_embed(author: discord.User, desc, color: discord.Color):
    embed = simple_embed("", desc, color)
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    return embed


def bj_template_embed(author: discord.User, player, desc: str, color: discord.Color):
    embed = authored_embed(author, desc, color)
    embed.set_thumbnail(url="https://www.vhv.rs/dpng/d/541-5416003_poker-club-ic"
                            "on-splash-diwali-coasters-black-background.png")
    card_string = "".join(card.emote for card in player.cards_owned)
    embed.add_field(name="Your hand", value=card_string)
    embed.set_footer(text="BlackJack",
                     icon_url="https://i.pinimg.com/originals/c3/5f/63/c35f630a4efb237206ec94f8950dcad5.png")
    return embed


def jack_embed(user: discord.User, player):
    embed = bj_template_embed(user, player, f"**Your bet: **{player.bet_amount}", discord.Color.gold())
    embed.add_field(name="Dealer hand", value=f"{player.game.dealer_cards[0].emote} + ?")
    return embed


def bj_win_embed(user: discord.User, player, show=False):
    embed = bj_template_embed(user, player, f"**Outcome: ** You won!\n"
                                            f"{player.bet_amount} is credited to your account.",
                              discord.Color.dark_green())
    if show is True:
        card_string = "".join(card.emote for card in player.game.dealer_cards)
        embed.add_field(name="Dealer's hand", value=card_string)
    else:
        embed.add_field(name="Dealer's hand", value=f"{player.game.dealer_cards[0].emote} + ?")
    return embed


def bj_bust_embed(user: discord.User, player, show=False):
    embed = bj_template_embed(user, player, f"**Outcome: ** You lost!\n"
                                            f"{player.bet_amount} is debited from your account.",
                              discord.Color.dark_red())
    if show is True:
        card_string = "".join(card.emote for card in player.game.dealer_cards)
        embed.add_field(name="Dealer's hand", value=card_string)
    else:
        embed.add_field(name="Dealer's hand", value=f"{player.game.dealer_cards[0].emote} + ?")
    return embed


def bj_push_embed(user: discord.User, player):
    embed = bj_template_embed(user, player, f"**Outcome: ** Its a tie!\n"
                                            f"{player.bet_amount} is added back to your account.",
                              discord.Color.dark_blue())
    card_string = "".join(card.emote for card in player.game.dealer_cards)
    embed.add_field(name="Dealer's hand", value=card_string)
    return embed


def fp_template_embed(user: discord.User):
    embed = authored_embed(author=user, desc="", color=discord.Color.gold())
    embed.title = "Flower Poker"
    embed.set_thumbnail(url="https://mpng.subpng.com/20200123/zbp/transpa"
                            "rent-poker-icon-casino-icon-lotto-icon-5e29a1b1654394.2050698115797866734148.jpg")
    embed.set_footer(text="react below to plant flowers")

    return embed


def fp_embed(user: discord.User, player, hidden=False):

    embed = fp_template_embed(user)
    flower_string = get_flower_string(player, hidden=hidden)
    embed.add_field(name="Your flowers", value=flower_string)
    flower_string = get_flower_string(player.game, hidden=hidden)
    embed.add_field(name="Dealer's flower", value=flower_string)
    return embed


def fp_win_embed(user: discord.User, player):
    embed = fp_embed(user, player)
    embed.colour = discord.Color.dark_green()
    embed.description = f"**Outcome: **You won {player.bet_amount}!\n" \
                        f"your {player.pair_count} pair beats dealer's {player.game.pair_count}"
    return embed


def fp_lose_embed(user: discord.User, player):
    embed = fp_embed(user, player)
    embed.colour = discord.Color.dark_red()
    embed.description = f"**Outcome: **You lost {player.bet_amount}!\n" \
                        f"Dealer's {player.game.pair_count} pair beats your {player.pair_count}"
    return embed


def fp_tie_embed(user: discord.User, player):
    embed = fp_embed(user, player)
    embed.description = f"**Outcome: **Its a tie!\n" \
                        f"Both of you have {player.game.pair_count} pairs"
    return embed
