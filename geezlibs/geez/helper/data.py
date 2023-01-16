from pyrogram.types import InlineKeyboardButton, WebAppInfo
from Geez.helper.cmd import PREFIX

class Data:

    text_help_menu = (
        "**Command List & Help**\n**Prefixes:** {PREFIX}"
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
    )
    reopen = [[InlineKeyboardButton("Re-Open", callback_data="reopen")]]
