from bot.configs.constants import default_blank_emote


def get_emote_list_string(item_list, hidden=False):
    if not hidden:
        return " ".join(item.emote for item in item_list)
    return " ".join(default_blank_emote for item in item_list)


def get_flower_string(player, hidden=False):
    emote_string = get_emote_list_string(player.flowers, hidden=hidden)
    if hidden:
        return f"{emote_string}\n**Value:** ?"
    return f"{emote_string}\n**Value:** {player.pair_count}"
