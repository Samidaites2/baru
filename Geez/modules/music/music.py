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
import aiohttp
import aiofiles
import ffmpeg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from datetime import datetime
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from Python_ARQ import ARQ


from config import *
from Geez import *
from config import ARQ_API as arq
from geezlibs import *
from geezlibs.geez import *
from geezlibs.geez.utils import *
from Geez.modules.basic import add_command_help


# File raw music
raw_filename = 'input.raw'

queue = []  # This is where the whole song queue is stored
playing = False  # Tells if something is playing or not


@Client.on_message(filters.command(["join"], cmds) & filters.me)
async def join(client: Client, message: Message):
    if group_call.is_connected:
        await message.reply_text('Bot already joined!')
        return
    group_call.client = app
    await group_call.start(message.chat.id)
    await message.reply_text('Succsessfully joined!')


@Client.on_message(filters.command(["mute"], cmds) & filters.me)
async def mute(client: Client, message: Message):
    group_call.set_is_mute(is_muted=True)
    await message.reply_text('Succsessfully muted bot!')


@Client.on_message(filters.command(["unmute"], cmds) & filters.me)
async def unmute(client: Client, message: Message):
    group_call.set_is_mute(is_muted=False)
    await message.reply_text('Succsessfully unmuted bot!')


@Client.on_message(filters.command(["volume"], cmds) & filters.me)
async def volume(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('You forgot to pass volume (1-200)')

    await group_call.set_my_volume(volume=int(message.command[1]))
    await message.reply_text(f'Volume changed to {message.command[1]}')


@Client.on_message(filters.command(["end"], cmds) & filters.me)
async def stop(client: Client, message: Message):
    global playing
    group_call.stop_playout()
    queue.clear()
    playing = False
    await message.reply_text('Succsessfully end song!')


@Client.on_message(filters.command(["leave"], cmds) & filters.me)
async def leave(client: Client, message: Message):
    global playing
    if not group_call.is_connected:
        await message.reply_text('Bot already leaved!')
        return
    await group_call.stop()
    queue.clear()
    playing = False
    group_call.input_filename = ''
    await message.reply_text('Succsessfully leaved!')


@Client.on_message(filters.command(["play"], cmds) & filters.me)
async def queues(client: Client, message: Message):
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

@Client.on_message(filters.command(["skip"], cmds) & filters.me)
async def skip(client: Client, message: Message):
    global playing
    if len(queue) == 0:
        await message.reply_text("__**Queue Is Empty, Just Like Your Life.**__")
        return
    playing = False
    await message.reply_text("__**Skipped!**__")
    await play()


@Client.on_message(filters.command(["playlist"], cmds) & filters.me)
async def queue_list(client: Client, message: Message):
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


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run()
    os.remove(filename)


#Download song
async def download_and_transcode_song(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open('song.mp3', mode='wb')
                await f.write(await resp.read())
                await f.close()
    transcode("song.mp3")


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


# Generate cover for jiosaavn and deezer
async def generate_cover_square(requested_by, title, artist, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    image1 = Image.open("./background.png")
    image2 = Image.open("cache/foreground_square.png")
    image3 = changeImageSize(600, 500, image1)
    image4 = changeImageSize(600, 500, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("cache/font.otf", 20)
    draw.text((150, 380), f"Title: {title}", (255, 255, 255), font=font)
    draw.text((150, 405), f"Artist: {artist}", (255, 255, 255), font=font)
    draw.text(
        (150, 430),
        f"Duration: {duration} Seconds",
        (255, 255, 255),
        font=font,
    )

    draw.text(
        (150, 455),
        f"Played By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


# Generate cover for youtube

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("cache/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("cache/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text(
        (190, 590), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((190, 670),
        f"Played By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")
