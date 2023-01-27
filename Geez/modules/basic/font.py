# if you can read this, this meant you use code from Geez Ram Project
# this code is from somewhere else
# please dont hestitate to steal it
# because Geez and Ram doesn't care about credit
# at least we are know as well
# who Geez and Ram is
#
#
# kopas repo dan hapus credit, ga akan jadikan lu seorang developer
# ©2023 Geez & Ram Team
from pyrogram import Client, filters
from pyrogram.types import Message

from pyrogram import Client as gez 
from geezlibs.geez.utils import *
from Geez.modules.basic import add_command_help
from config import *
from Geez import cmds


arguments = [
    "smallcap",
    "monospace",
    "outline",
    "script",
    "blackbubbles",
    "bubbles",
    "bold",
    "bolditalic"
]

fonts = [
    "smallcap",
    "monospace",
    "outline",
    "script",
    "blackbubbles",
    "bubbles",
    "bold",
    "bolditalic"
]

_default = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_smallcap = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"
_monospace = "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"
_outline = "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
_script = "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"
_blackbubbles = "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"
_bubbles = "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
_bold = "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
_bolditalic = "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕"


def gen_font(text, new_font):
    new_font = " ".join(new_font).split()
    for q in text:
        if q in _default:
            new = new_font[_default.index(q)]
            text = text.replace(q, new)
    return text

def get_cmd(
        self,
        message: Message
    ):
        msg = message.text
        msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
        split = msg[1:].replace("\n", " \n").split(" ")
        if " ".join(split[1:]).strip() == "":
            return ""
        return " ".join(split[1:])

@gez.on_message(filters.command(["font"], cmds) & filters.me)
async def font_gz(client: Client, message: Message):
    if message.reply_to_message or msg.get_cmd(message):
        font = msg.get_cmd(message)
        text = message.reply_to_message.text
        if not font:
            return await edit_or_reply(message, f"<code>{font} Tidak Ada Dalam Daftar Font...</code>")
        if font == "smallcap":
            mmk = gen_font(text, _smallcap)
        elif font == "monospace":
            mmk = gen_font(text, _monospace)
        elif font == "outline":
            mmk = gen_font(text, _outline)
        elif font == "script":
            mmk = gen_font(text, _script)
        elif font == "blackbubbles":
            mmk = gen_font(text, _blackbubbles)
        elif font == "bubbles":
            mmk = gen_font(text, _bubbles)
        elif font == "bold":
            mmk = gen_font(text, _bold)
        elif font == "bolditalic":
            mmk = gen_font(text, _bolditalic)
        await edit_or_reply(message, mmk)

    else:
        return await message.reply("`Balas Teks Dan Isi Nama Font`")



@gez.on_message(filters.command(["lf"], cmds) & filters.me)
async def fonts(client: Client, msg: Message):
    await edit_or_reply(
        msg,
        "<b>❯❯ ᴅᴀғᴛᴀʀ ғᴏɴᴛs ❮❮</b>\n"
        "<b>• sᴍᴀʟʟᴄᴀᴘ</b>\n"
        "<b>• 𝚖𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎</b>\n"
        "<b>• 𝕠𝕦𝕥𝕝𝕚𝕟𝕖</b>\n"
        "<b>• 𝓈𝒸𝓇𝒾𝓅𝓉 </b>\n"
        "<b>• 🅑🅛🅐🅒🅚🅑🅤🅑🅑🅛🅔🅢</b>\n"
        "<b>• ⓑⓤⓑⓑⓛⓔⓢ</b>\n"
        "<b>• 𝗯𝗼𝗹𝗱</b>\n"
        "<b>• 𝙗𝙤𝙡𝙙𝙞𝙩𝙖𝙡𝙞𝙘</b>\n\n"
    )


add_command_help(
    "Fonts",[
        [f"{cmds}font", "Membuat Text Dengan Gaya Font Berbeda",],
        [f"{cmds}lf", "Untuk Melihat Daftar Font."],
    ],
)


