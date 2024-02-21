import discord
from discord.ext import commands
import os
import logging
import asyncio
import psutil
from dotenv import load_dotenv
from anilist import AnilistDiscord
from handler import DiscordHandler
from keep_alive import keep_alive

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='/', intents=intents)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

logger = logging.getLogger()
discord_format = logging.Formatter("%(message)s")
file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(discord_format)
discord_handler = DiscordHandler("Lisa Logs", WEBHOOK_URL,
                                 avatar_url="https://www.linkpicture.com/q/peakpx-2_11.jpg")
discord_handler.setFormatter(discord_format)
logger.addHandler(discord_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def send_log_message(level, message):
    if level == 'info':
        logger.info(message)
    elif level == 'debug':
        logger.debug(message)
    elif level == 'error':
        logger.error(message)
    else:
        raise ValueError("Invalid log level")

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print("Bot is now online!")


@bot.command(name="logs")
async def logs(ctx, option=None):
    """Get Logs"""
    if option == "clear":
        open("logs.log", "w").close()
        message = await ctx.send(embed=discord.Embed(
            description="Logs Cleared.", colour=discord.Colour.orange()))
        await asyncio.sleep(10)
        await message.delete()
    else:
        if not os.path.isfile("logs.log") or os.stat("logs.log").st_size == 0:
            await ctx.send("Log file not located.")
            return

        file = discord.File("logs.log")
        await ctx.send(file=file)


@bot.command()
async def purge(ctx, amount=1000):
    """Purge Server messages."""
    note = "Messages purged."
    channel_id = int(os.getenv("channelId"))
    if ctx.channel.id == channel_id:
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        message = await ctx.send(
            embed=discord.Embed(description=note, colour=discord.Colour.orange()))
        await asyncio.sleep(10)
        await message.delete()
    else:
        pass


@bot.command()
async def clear(ctx):
    """Clear Server Messages"""
    guild = ctx.guild
    channel_id = int(os.getenv("channelId"))

    if ctx.channel.id == channel_id:
        selected_message = None
        async for message in ctx.channel.history(limit=None):
            if message.author == ctx.author:
                selected_message = message
                break

        if selected_message:
            await selected_message.delete()
            await asyncio.sleep(1)

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).manage_messages:
                try:
                    async for message in channel.history(limit=None):
                        await message.delete()
                        await asyncio.sleep(1)
                except discord.NotFound:
                    pass
                except discord.HTTPException:
                    await asyncio.sleep(1)
                    continue

    embed = discord.Embed(description="All messages have been cleared.",
                          colour=discord.Colour.greyple())
    message = await ctx.send(embed=embed)
    await asyncio.sleep(10)
    await message.delete()

@bot.command()
async def stats(ctx):
    """System stats"""
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    status_message = f"CPU Usage: {cpu_usage}%\nMemory Usage: {memory_usage}%"
    embed = discord.Embed(description=status_message,
                          colour=discord.Colour.blue())
    message = await ctx.send(embed=embed)
    await asyncio.sleep(5)
    await message.delete()

# Search anime
@bot.command()
async def anime(ctx):
    """Search Anime"""
    message_content = ctx.message.content[len("/anime") + 1:]
    anime_embed = AnilistDiscord.get_anime_discord(anime_name=message_content)
    if anime_embed == -1:
        await ctx.send(
            "Anime not found! Please try again or use a different name. (romaji preferred)"
        )
    else:
        await ctx.send(embed=anime_embed)


mangaList = [
    'name_romaji', 'name_english', 'starting_time', 'ending_time',
    'release_format', 'release_status', 'chapters', 'volumes', 'desc',
    'average_score', 'mean_score', 'genres', 'synonyms'
]


@bot.command()
async def manga(ctx):
    """Search Manga"""
    message_content = ctx.message.content[len("/manga") + 1:]
    mangaInfo = AnilistDiscord.get_manga_info(message_content)
    print(f'manga {mangaInfo}')
    if mangaInfo == '':
        await ctx.send(
            "Manga not found! Please try again or use a different name. (romaji preferred)"
        )
    else:
        embed = discord.Embed()
        embed.title = mangaInfo['name_romaji']
        embed.description = mangaInfo['name_english']
        embed.color = 0xA0DB8E
        embed.set_image(url=mangaInfo['banner_image'])
        embed.set_thumbnail(url=mangaInfo['cover_image'])

        for key in mangaList:
            value = mangaInfo[key]
            if value:
                embed.add_field(name=key, value=value, inline=False)
        await ctx.send(embed=embed)

keep_alive()

bot.run(DISCORD_BOT_TOKEN, log_handler=discord_handler)