import discord
from discord import Embed


def simple_embed(desc):
    return Embed(title="", description=desc, color=discord.Color.blue())


def jack_embed(user: discord.User, player):
    embed = Embed(title="", description=f"**Your bet: **{player.bet_amount}", color=discord.Color.gold())
    embed.set_thumbnail(url="https://www.vhv.rs/dpng/d/541-5416003_poker-club-icon-splash-diwali-coasters-black-background.png")
    embed.set_author(name=user.name, icon_url=user.avatar_url)
    card_string = "".join(card.emote for card in player.cards_owned)
    embed.add_field(name="Your hand", value=card_string)
    embed.add_field(name="Dealer hand", value=f"{player.game.dealer_cards[0].emote} + ?")
    embed.set_footer(text="BlackJack", icon_url="https://i.pinimg.com/originals/c3/5f/63/c35f630a4efb237206ec94f8950dcad5.png")
    return embed


def bj_win_embed(user: discord.User, player):
    embed = Embed(title="BlackJack!", description=f"**Outcome: ** You won!\n{player.bet_amount} is "
                                                  f"credited to your account.",
                  color=discord.Color.green())
    embed.set_thumbnail(url="https://www.vhv.rs/dpng/d/541-5416003_poker-club-icon-splash-diwali-coasters-black-background.png")
    embed.set_author(name=user.name, icon_url=user.avatar_url)
    card_string = "".join(card.emote for card in player.cards_owned)
    embed.add_field(name="Your hand", value=card_string)
    card_string = "".join(card.emote for card in player.game.dealer_cards)
    embed.add_field(name="Dealer hand", value=card_string)
    embed.set_footer(text="BlackJack", icon_url="https://i.pinimg.com/originals/c3/5f/63/c35f630a4efb237206ec94f8950dcad5.png")
    return embed


def bj_bust_embed(user: discord.User, player):
    embed = Embed(title="Busted!", description=f"**Outcome: ** You lost!\n\n{player.bet_amount} is debited from your"
                                               f"account",
                  color=discord.Color.red())
    embed.set_thumbnail(url="https://www.vhv.rs/dpng/d/541-5416003_poker-club-icon-splash-diwali-coasters-black-background.png")
    embed.set_author(name=user.name, icon_url=user.avatar_url)
    card_string = "".join(card.emote for card in player.cards_owned)
    embed.add_field(name="Your hand", value=card_string)
    embed.add_field(name="Dealer's hand", value=f"{player.game.dealer_cards[0].emote} + ?")
    embed.set_footer(text="BlackJack", icon_url="https://i.pinimg.com/originals/c3/5f/63/c35f630a4efb237206ec94f8950dcad5.png")
    return embed