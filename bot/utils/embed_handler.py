import discord  # noqa
from discord import Embed  # noqa


def simple_embed(desc, color=discord.Color.blue()):
    return Embed(title="", description=desc, color=color)


def authored_embed(author: discord.User, player, desc: str, color: discord.Color):
    embed = simple_embed(desc, color)
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    embed.set_thumbnail(url="https://www.vhv.rs/dpng/d/541-5416003_poker-club-ic"
                            "on-splash-diwali-coasters-black-background.png")
    card_string = "".join(card.emote for card in player.cards_owned)
    embed.add_field(name="Your hand", value=card_string)
    embed.set_footer(text="BlackJack",
                     icon_url="https://i.pinimg.com/originals/c3/5f/63/c35f630a4efb237206ec94f8950dcad5.png")
    return embed


def jack_embed(user: discord.User, player):
    embed = authored_embed(user, player, f"**Your bet: **{player.bet_amount}", discord.Color.gold())
    embed.add_field(name="Dealer hand", value=f"{player.game.dealer_cards[0].emote} + ?")
    return embed


def bj_win_embed(user: discord.User, player, show=False):
    embed = authored_embed(user, player, f"**Outcome: ** You won!\n"
                                         f"{player.bet_amount} is credited to your account.",
                           discord.Color.dark_green())
    if show is True:
        card_string = "".join(card.emote for card in player.game.dealer_cards)
        embed.add_field(name="Dealer's hand", value=card_string)
    else:
        embed.add_field(name="Dealer's hand", value=f"{player.game.dealer_cards[0].emote} + ?")
    return embed


def bj_bust_embed(user: discord.User, player, show=False):
    embed = authored_embed(user, player, f"**Outcome: ** You lost!\n"
                                         f"{player.bet_amount} is debited from your account.",
                           discord.Color.dark_red())
    if show is True:
        card_string = "".join(card.emote for card in player.game.dealer_cards)
        embed.add_field(name="Dealer's hand", value=card_string)
    else:
        embed.add_field(name="Dealer's hand", value=f"{player.game.dealer_cards[0].emote} + ?")
    return embed


def bj_push_embed(user: discord.User, player):
    embed = authored_embed(user, player, f"**Outcome: ** Its a tie!\n"
                                         f"{player.bet_amount} is added back to your account.",
                           discord.Color.dark_red())
    card_string = "".join(card.emote for card in player.game.dealer_cards)
    embed.add_field(name="Dealer's hand", value=card_string)
    return embed
