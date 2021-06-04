"""
VidCha Discord Bot
This bot will annouce you if your youtube channel that's you subscribe have a new video. :)
"""

import os
import json
import discord
import requests
import xmltodict
import datetime

from dotenv import load_dotenv
from discord.ext import commands, tasks


from model import *

"""
Initialize
"""

load_dotenv()

TOKEN = os.environ.get("DISCORD_TOKEN")
YT_API_KEY = os.environ.get("YOUTUBE_API_KEY")
BOT_NAME = os.environ.get("DISCORD_BOT_NAME", "VidCha")
PREFIX = os.environ.get("COMMAND_PREFIX")
UPDATE_INTERVAL = int(os.environ.get("RSS_UPDATE_INTERVAL"))

client = commands.Bot(PREFIX)
# bot = commands.Bot(PREFIX)

client.remove_command('help')

def p_command(command: str) -> str:
    return PREFIX + command


"""
Handeling Youtube things
"""

def get_channel_data_from_id(channel_id):
    req = requests.get("https://www.youtube.com/feeds/videos.xml?channel_id=" + channel_id)

    if req.status_code != 200:
        return None

    channel_data = xmltodict.parse(req.text)

    return channel_data.get('feed', None)

def get_channel_image_url(channel_id):
    req = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&fields=items%2Fsnippet%2Fthumbnails&key={YT_API_KEY}")
    items = json.loads(req.text)
    try:
        return items['items'][0]['snippet']['thumbnails']['high']['url']
    except:
        return None # LOL, DON'T DO THIS WITH YOUR COMPANY'S WORK :P

def search_for_channel_id(keyword):
    req = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?part=id&part=snippet&q={keyword}&type=channel&key={YT_API_KEY}")
    items = json.loads(req.text)['items']
    if len(items) > 0:
        return items[0]['id']['channelId']
    return None

def is_channel_id(c_id: str) -> bool:
    req = requests.get("https://www.youtube.com/feeds/videos.xml?channel_id=" + c_id)
    return req.status_code == 200

def get_last_vid(feed):
    return feed.get('entry')[0]['yt:videoId'] if feed.get('entry') is not None else None


def get_need_to_notify_vids(feed, last_notify_id):
    videos = []
    for entry in feed.get('entry', []):

        # time diff is less than 10 minutes
        published_time = datetime.datetime.strptime(entry['published'], "%Y-%m-%dT%H:%M:%S+00:00")
        current_time = datetime.datetime.utcnow()

        if (current_time - published_time).seconds > 600:
            break

        # is not notified video
        if entry['yt:videoId'] == last_notify_id:
            break

        videos.append(entry)

    return videos
        

def get_yt_channel(channel_things: str):

    # maybe this is url
    if "youtube" in channel_things or \
       "http://" in channel_things or \
       "https://" in channel_things or \
       "/c/" in channel_things or \
       "/" in channel_things or \
       "/channel/" in channel_things:
        channel_id_or_name = channel_things.split('/')[-1]
        
        if is_channel_id(channel_id_or_name):
            return get_channel_data_from_id(channel_id_or_name)
        
        channel_id = search_for_channel_id(channel_id_or_name)
        
        if channel_id is None:
            return None
        return get_channel_data_from_id( channel_id )

    if is_channel_id(channel_things):
        return get_channel_data_from_id(channel_things)

    channel_id = search_for_channel_id(channel_things)
        
    if channel_id is None:
        return None

    return get_channel_data_from_id( channel_id )

"""
Handeling all commands
"""

@client.command()
async def author(ctx):
    embed=discord.Embed(title="Owner of VidCha Bot", url="https://github.com/n0uur", description="หากมีข้อสงสัย หรือมีปัญหากับบอทติดต่อได้ที่", color=0x00ffcc)
    embed.set_author(name="n0uur", url="https://github.com/n0uur")
    embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/50010805?v=4")
    embed.add_field(name="Github", value="n0uur", inline=True)
    embed.add_field(name="Facebook", value="fb.me/0ktnn", inline=True)
    embed.set_footer(text="https://github.com/n0uur/vidcha-bot")
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):

    command_text = f"""`{p_command('help')}` แสดงรายการคำสั่งที่ใช้งานได้
    `{p_command('sub')} <Youtube Channel NAME/ID>` เพื่อติดตามช่อง (ใส่หลายช่องได้ โดยแบ่งด้วยเว้นวรรค)
    `{p_command('unsub')} <Youtube Channel NAME/ID>` เพื่อยกเลิกติดตามช่อง (ใส่หลายช่องได้ โดยแบ่งด้วยเว้นวรรค)
    `{p_command('unsub')} all` เพื่อยกเลิกติดตามช่องทั้งหมดที่ติดตามอยู่
    `{p_command('list')}` ดูรายการช่อง Youtube ที่ติดตามอยู่
    `{p_command('author')}` ดูข้อมูลเจ้าของ Bot <3
    \n\n:warning: หากชื่อช่องมีเว้นวรรค ให้ใส่ฟันหนูครอบ เช่น `{p_command('sub')} "Bay Riffer"`
    """

    embed=discord.Embed(title=":gear: คำสั่งที่สามารถใช้งานได้", color=0x00ffcc)
    embed.add_field(name=f"พิมพ์ ```{PREFIX}``` ตามด้วยคำสั่งเพื่อเรียกใช้งาน", value=command_text, inline=True)
    embed.set_footer(text="https://github.com/n0uur/vidcha-bot")
    await ctx.send(embed=embed)

@client.command()
async def sub(ctx, *args):
    
    for yt_channel in args:

        yt_feed = get_yt_channel(yt_channel)

        if yt_feed is None:
            await ctx.send("ไม่พบช่องที่ต้องการติดตาม :x:")
            return

        yt_channel_id, yt_channel_name = yt_feed['yt:channelId'], yt_feed['title']

        # todo: add subscription limit like 10 or 20 channels :)

        is_exists = Subscription.select().where(
            (Subscription.channel_id == ctx.channel.id) & (Subscription.youtube_id == yt_channel_id)
        ).exists()
        
        if is_exists:
            await ctx.send("มีการติดตามช่องนี้อยู่แล้ว :x:")
            return

        yt_channel = YoutubeChannel.select().where(
            YoutubeChannel.youtube_id == yt_channel_id
        )

        if not yt_channel.exists():
            yt_channel = YoutubeChannel.create(
                youtube_id = yt_channel_id,
                youtube_name = yt_channel_name,
                youtube_image = get_channel_image_url(yt_channel_id),
                youtube_last_notify_vid = get_last_vid(yt_feed)
            )
        else:
            yt_channel = yt_channel.first()
            yt_channel.youtube_last_notify_vid = get_last_vid(yt_feed)  # this is may cause race condition, but who cares ?
            yt_channel.save()

        subscription = Subscription.create(
            channel_id = ctx.channel.id,
            youtube_id = yt_channel_id,
        )

        embed=discord.Embed(title=yt_channel_name, url=yt_feed['link'][1]['@href'], description=f"ติดตามช่อง {yt_channel_name} เรียบร้อยแล้ว")
        embed.set_thumbnail(url=yt_channel.youtube_image)

        await ctx.send(f"ติดตาม `{yt_channel_name}` แล้ว :smile:", embed=embed)

@client.command()
async def unsub(ctx, *args):

    if len(args) and args[0] == "all":
        subscription_query = Subscription.delete().where(
                Subscription.channel_id == ctx.channel.id
            )
        subscription_query.execute()

        await ctx.send("ยกเลิกการติดตามทั้งหมดแล้ว :cry:")

        return

    for yt_channel in args:

        yt_feed = get_yt_channel(yt_channel)

        if yt_feed is None:
            await ctx.send("ไม่พบช่องที่ต้องการติดตาม :x:")
            return

        yt_channel_id, yt_channel_name = yt_feed['yt:channelId'], yt_feed['title']

        subscription = Subscription.select(Subscription, YoutubeChannel.youtube_name).join(
            YoutubeChannel, on=(Subscription.youtube_id == YoutubeChannel.youtube_id)
            ).where(
                (Subscription.channel_id == ctx.channel.id) & (Subscription.youtube_id == yt_channel_id)
            )
        
        if not subscription.exists():
            await ctx.send("ไม่พบการติดตามช่องนี้ :x:")
            return

        await ctx.send(f"ยกเลิกการติดตาม `{subscription.first().youtubechannel.youtube_name}` แล้ว :cry:")

        subscription.first().delete_instance()

@client.command()
async def list(ctx):

    subscriptions_query = Subscription.select(Subscription, YoutubeChannel).join(
        YoutubeChannel, on=(Subscription.youtube_id == YoutubeChannel.youtube_id)
    ).where(
        Subscription.channel_id == ctx.channel.id
    )

    yt_channels = [
        {
            "yt_channel_image": subscription.youtubechannel.youtube_image,
            "yt_channel_name": subscription.youtubechannel.youtube_name,
            "yt_channel_id": subscription.youtubechannel.youtube_id,
        }
        for subscription in subscriptions_query.execute()
    ]

    yt_count = len(yt_channels)

    list_text = ""

    for index, channel in enumerate(yt_channels):
        list_text += f"{index + 1}). ช่อง `{channel['yt_channel_name']}`"
        if yt_count <= 8:
            list_text += f"ID: `{channel['yt_channel_id']}`"
        list_text += "\n"
    
    if yt_count == 0:
        list_text = f"คุณยังไม่มีช่องที่ติดตามเลย :cry:\nพิมพ์ `{p_command('help')}` เพื่อดูวิธีใช้"

    for_move_text = f"```{p_command('sub')} {' '.join([i['yt_channel_id'] for i in yt_channels])}```"

    embed=discord.Embed(title=":notebook_with_decorative_cover: รายชื่อช่องที่ติดตามอยู่", color=0x00ffcc)
    embed.add_field(name=f"กำลังติดตามอยู่ทั้งหมด `{yt_count}` ช่อง", value=list_text, inline=False)
    if yt_count > 0:
        embed.add_field(name=f"คำสั่งสำหรับนำไปติดตามที่ Discord อื่น ๆ", value=for_move_text, inline=False)
    embed.set_footer(text="https://github.com/n0uur/vidcha-bot")
    await ctx.send(embed=embed)

"""
Handeling all events
"""

@client.event
async def on_ready():
    """
    Bot connected to Discord server
    """
    print(f"Hello :) I'm {client.user}. connected to discord headquarter via WebSocket!")
    await client.change_presence(activity=discord.Game(name=f"use '{p_command('help')}' to show all commands! <3"))
    check_for_updates.start()

@client.event
async def on_message(message):
    """
    Handeling all message that's I see
    """

    if message.author == client.user:  # do not talk to yourself. it's not good for Bot :(
        return

    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send("ไม่คุยส่วนตัวด้วยหรอกนะคะ มีอะไรรบกวนพิมพ์ในห้องนะ 🤪")
        return

    await client.process_commands(message)

"""
Main Bot Loop
"""

async def multicast(d_channels: list, video):

    yt_channel_name = video['author']['name']
    yt_link = video['link']['@href']

    message = f":hand_splayed: โย่ววววว, `{yt_channel_name}` มีวิดิโอมาใหม่ ไปดูกันด้วยยยยย\n{yt_link}"
    
    for channel in d_channels:
        _channel = client.get_channel(channel)
        if _channel:
            await _channel.send(message)

@tasks.loop(seconds=UPDATE_INTERVAL)
async def check_for_updates():
    yt_channels = YoutubeChannel.select(YoutubeChannel).distinct().join(
            Subscription, on=(YoutubeChannel.youtube_id == Subscription.youtube_id)
        )  # channels that's still have subscriptions

    for channel in yt_channels:
        
        channel_feed = get_channel_data_from_id(channel.youtube_id)

        if channel_feed is None: # maybe it's just broken da broken
            continue

        last_video_id = get_last_vid(channel_feed)

        if channel.youtube_last_notify_vid == last_video_id:  # still no new update
            continue

        new_vids =  get_need_to_notify_vids(
                        channel_feed,
                        channel.youtube_last_notify_vid
                    )

        new_vids.reverse()
        
        subscriptions = Subscription.select(Subscription.channel_id).distinct().where(
            Subscription.youtube_id == channel.youtube_id
        )

        for video in new_vids:
            await multicast(
                [subscription.channel_id for subscription in subscriptions],
                video
            )

        channel.youtube_last_notify_vid = last_video_id
        channel.save()

"""
Bot ignition, brrmm! brrmm!
"""

if __name__ == "__main__":
    DATABASE.connect()
    client.run(TOKEN)
    DATABASE.close()
