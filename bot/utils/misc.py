from bot.configs.constants import default_blank_emote


def get_emote_list_string(item_list, hidden=False):
    if not hidden:
        return "".join(item.emote for item in item_list)
    return "".join(default_blank_emote for item in item_list)
