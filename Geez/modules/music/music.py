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
import asyncio
import os
import youtube_dl

from datetime import datetime
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from Python_ARQ import ARQ

from .functions import (
    transcode,
    download_and_transcode_song,
    convert_seconds,
    time_to_seconds,
    generate_cover,
    generate_cover_square
)

from config import *
from Geez import *
from geezlibs import *
from geezlibs.geez import *
from geezlibs.geez.utils import *
from Geez.modules.basic import add_command_help


group_call = GroupCallFactory(None, path_to_log_file='')

# Arq Client
arq = ARQ(ARQ_API)

# File raw music
raw_filename = 'input.raw'

queue = []  # This is where the whole song queue is stored
playing = False  # Tells if something is playing or not


@app.on_message(filters.command("join", cmds) & filters.me)
async def join(_, message):
    if group_call.is_connected:
        await message.reply_text('Bot already joined!')
        return
    group_call.client = app
    await group_call.start(message.chat.id)
    await message.reply_text('Succsessfully joined!')


@app.on_message(filters.command("mute", cmds) & filters.me)
async def mute(_, message):
    group_call.set_is_mute(is_muted=True)
    await message.reply_text('Succsessfully muted bot!')


@app.on_message(filters.command("unmute", cmds) & filters.me)
async def unmute(_, message):
    group_call.set_is_mute(is_muted=False)
    await message.reply_text('Succsessfully unmuted bot!')


@app.on_message(filters.command("volume", cmds) & filters.me)
async def volume(_, message):
    if len(message.command) < 2:
        await message.reply_text('You forgot to pass volume (1-200)')

    await group_call.set_my_volume(volume=int(message.command[1]))
    await message.reply_text(f'Volume changed to {message.command[1]}')


@app.on_message(filters.command("end", cmds) & filters.me)
async def stop(_, message):
    global playing
    group_call.stop_playout()
    queue.clear()
    playing = False
    await message.reply_text('Succsessfully end song!')


@app.on_message(filters.command("leave", cmds) & filters.me)
async def leave(_, message):
    global playing
    if not group_call.is_connected:
        await message.reply_text('Bot already leaved!')
        return
    await group_call.stop()
    queue.clear()
    playing = False
    group_call.input_filename = ''
    await message.reply_text('Succsessfully leaved!')


@app.on_message(filters.command("play", cmds) & filters.me)
async def queues(_, message):
    if not group_call.is_connected:
        await message.reply_text('Bot not joined on Voice Calls!')
        return
    usage = "**Usage:**\n__**{cmds}play  Song_Name**__"
    if len(message.command) < 3:
        await message.reply_text(usage)
        return
    text = message.text.split(None, 2)[1:]
    service = text[0]
    song_name = text[1]
    requested_by = message.from_user.first_name
    services = ["youtube", "deezer", "saavn"]
    if service not in services:
        await message.reply_text(usage)
        return
    if len(queue) > 0:
        await message.reply_text("__**Added To Queue.__**")
        queue.append({"service": service, "song": song_name,
                      "requested_by": requested_by})
        await play()
        return
    queue.append({"service": service, "song": song_name,
                  "requested_by": requested_by})
    await play()

@app.on_message(filters.command("skip", cmds) & filters.me)
async def skip(_, message):
    global playing
    if len(queue) == 0:
        await message.reply_text("__**Queue Is Empty, Just Like Your Life.**__")
        return
    playing = False
    await message.reply_text("__**Skipped!**__")
    await play()


@app.on_message(filters.command("playlist", cmds) & filters.me)
async def queue_list(_, message):
    if len(queue) != 0:
        i = 1
        text = ""
        for song in queue:
            text += f"**{i}. Platform:** __**{song['service']}**__ | **Song:** __**{song['song']}**__\n"
            i += 1
        await message.reply_text(text)
    else:
        await message.reply_text("__**Queue Is Empty, Just Like Your Life.**__")

# Queue handler

async def play():
    global queue, playing
    while not playing:
        await asyncio.sleep(2)
        if len(queue) != 0:
            service = queue[0]["service"]
            song = queue[0]["song"]
            requested_by = queue[0]["requested_by"]
            if service == "youtube":
                playing = True
                del queue[0]
                try:
                    await ytplay(requested_by, song)
                except Exception as e:
                    print(str(e))
                    await send(str(e))
                    playing = False
            elif service == "saavn":
                playing = True
                del queue[0]
                try:
                    await jiosaavn(requested_by, song)
                except Exception as e:
                    print(str(e))
                    await send(str(e))
                    playing = False
            elif service == "deezer":
                playing = True
                del queue[0]
                try:
                    await deezer(requested_by, song)
                except Exception as e:
                    print(str(e))
                    await send(str(e))
                    playing = False


# Deezer----------------------------------------------------------------------------------------

async def deezer(requested_by, query):
    global playing
    m = await send(f"__**Searching for {query} on Deezer.**__")
    try:
        songs = await arq.deezer(query, 1)
        title = songs[0].title
        duration = convert_seconds(int(songs[0].duration))
        thumbnail = songs[0].thumbnail
        artist = songs[0].artist
        url = songs[0].url
    except Exception as e:
        await m.edit("__**Found No Song Matching Your Query.**__")
        playing = False
        print(str(e))
        return
    await m.edit("__**Generating Thumbnail.**__")
    await generate_cover_square(requested_by, title, artist, duration, thumbnail)
    await m.edit("__**Downloading And Transcoding.**__")
    await download_and_transcode_song(url)
    await m.delete()
    m = await app.send_photo(
        chat_id=SUDO_USER,
        photo="final.png",
        caption=f"**Playing** __**[{title}]({url})**__ **Via Deezer.**",
    )
    os.remove("final.png")
    group_call.input_filename = raw_filename
    await asyncio.sleep(int(songs[0]["duration"]))
    await m.delete()
    playing = False


# Jiosaavn--------------------------------------------------------------------------------------


async def jiosaavn(requested_by, query):
    global playing
    m = await send(f"__**Searching for {query} on JioSaavn.**__")
    try:
        songs = await arq.saavn(query)
        sname = songs[0].song
        slink = songs[0].media_url
        ssingers = songs[0].singers
        sthumb = songs[0].image
        sduration = songs[0].duration
        sduration_converted = convert_seconds(int(sduration))
    except Exception as e:
        await m.edit("__**Found No Song Matching Your Query.**__")
        print(str(e))
        playing = False
        return
    await m.edit("__**Processing Thumbnail.**__")
    await generate_cover_square(
        requested_by, sname, ssingers, sduration_converted, sthumb
    )
    await m.edit("__**Downloading And Transcoding.**__")
    await download_and_transcode_song(slink)
    await m.delete()
    m = await app.send_photo(
        chat_id=SUDO_USER,
        caption=f"**Playing** __**{sname}**__ **Via Jiosaavn.**",
        photo="final.png",
    )
    os.remove("final.png")
    group_call.input_filename = raw_filename
    await asyncio.sleep(int(sduration))
    await m.delete()
    playing = False


# Youtube Play-----------------------------------------------------------------------------------


async def ytplay(requested_by, query):
    global playing
    ydl_opts = {"format": "bestaudio"}
    m = await send(f"__**Searching for {query} on YouTube.**__")
    try:
        results = await arq.youtube(query, 1)
        link = f"https://youtube.com{results[0].url_suffix}"
        title = results[0].title
        thumbnail = results[0].thumbnails[0]
        duration = results[0].duration
        views = results[0].views
        if time_to_seconds(duration) >= 1800:
            await m.edit("__**Bruh! Only songs within 30 Mins.**__")
            playing = False
            return
    except Exception as e:
        await m.edit("__**Found No Song Matching Your Query.**__")
        playing = False
        print(str(e))
        return
    await m.edit("__**Processing Thumbnail.**__")
    await generate_cover(requested_by, title, views, duration, thumbnail)
    await m.edit("__**Downloading Music.**__")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=False)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)
    await m.edit("__**Transcoding.**__")
    os.rename(audio_file, "audio.webm")
    transcode("audio.webm")
    await m.delete()
    m = await app.send_photo(
        chat_id=SUDO_USER,
        caption=f"**Playing** __**[{title}]({link})**__ **Via YouTube.**",
        photo="final.png",
    )
    os.remove("final.png")
    group_call.input_filename = raw_filename
    await asyncio.sleep(int(time_to_seconds(duration)))
    playing = False
    await m.delete()

async def send(text):
    m = await app.send_message(SUDO_USER, text=text, disable_web_page_preview=True)
    return m

print('[INFO] Bot is running...\n')
app.run()
