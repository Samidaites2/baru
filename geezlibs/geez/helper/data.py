from pyrogram.types import InlineKeyboardButton, WebAppInfo
from Geez.helper.cmd import cmd

class Data:

    text_help_menu = (
        "**Command List & Help**\n**Prefixes:** {cmd}"
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
    )
    reopen = [[InlineKeyboardButton("Re-Open", callback_data="reopen")]]
