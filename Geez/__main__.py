import importlib
from pyrogram import idle
from uvloop import install

from config import CMD_HNDLR
from Geez.modules import ALL_MODULES
from Geez import BOTLOG_CHATID, LOGGER, LOOP, aiosession, bot1, bots, app, ids
from geezlibs import join
from geezlibs import BOT_VER, __version__ as gver
MSG_ON = """
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
**Premium Userbot Actived ✅**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
"""


async def main():
    await app.start()
    print("Memulai Premium Userbot..")
    print("Loading Everything.")
    for all_module in ALL_MODULES:
        importlib.import_module("Geez.modules" + all_module)
        print(f"Successfully Imported {all_module} ")
    for bot in bots:
        try:
            await bot.start()
            ex = await bot.get_me()
            await join(bot)
            try:
                await bot.send_message(BOTLOG_CHATID, MSG_ON)
            except BaseException:
                pass
            print(f"Started as {ex.first_name} | {ex.id} ")
            ids.append(ex.id)
        except Exception as e:
            print(f"{e}")
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("✅").info("Starting Premium Userbot")
    install()
    LOOP.run_until_complete(main())
