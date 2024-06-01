import discord
from discord.ext import commands
import os
import logging
import asyncio
import psutil
from dotenv import load_dotenv
from handler import DiscordHandler
from keep_alive import keep_alive
from AnilistPython import Anilist

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

anilist = Anilist()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

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

@bot.event
async def on_ready():
    print("Bot is now online!")

@bot.command(name="logs")
async def logs(ctx, option=None):
    """Get Logs"""
    try:
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
    except Exception as e:
        send_log_message('error', f"Error in logs command: {e}")
        await ctx.send("An error occurred while handling the logs command.")

@bot.command(name="purge")
async def purge(ctx, amount=1000):
    """Purge Server messages."""
    try:
        note = "Messages purged."
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        message = await ctx.send(
                embed=discord.Embed(description=note, colour=discord.Colour.orange()))
        await asyncio.sleep(10)
        await message.delete()
    except Exception as e:
        send_log_message('error', f"Error in purge command: {e}")
        await ctx.send("An error occurred while purging messages.")

@bot.command(name="clear")
async def clear(ctx):
    """Clear Server Messages"""
    try:
        guild = ctx.guild

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
    except Exception as e:
        send_log_message('error', f"Error in clear command: {e}")
        await ctx.send("An error occurred while clearing messages.")

@bot.command(name="stats")
async def stats(ctx):
    """System stats"""
    try:
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        status_message = f"CPU Usage: {cpu_usage}%\nMemory Usage: {memory_usage}%"
        embed = discord.Embed(description=status_message,
                              colour=discord.Colour.blue())
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()
    except Exception as e:
        send_log_message('error', f"Error in stats command: {e}")
        await ctx.send("An error occurred while fetching system stats.")

@bot.command(name="anime")
async def anime(ctx):
    """Search Anime"""
    message_content = ctx.message.content[len("/anime") + 1:]
    try:
        anime_dict = anilist.get_anime(anime_name=message_content)
    except Exception as e:
        send_log_message('error', f"Error fetching anime: {e}")
        return await ctx.send("An error occurred while fetching anime information.")

    try:
        eng_name = anime_dict.get("name_english", "")
        jap_name = anime_dict.get("name_romaji", "")
        desc = anime_dict.get("desc", "")
        starting_time = anime_dict.get("starting_time", "")
        ending_time = anime_dict.get("ending_time", "")
        cover_image = anime_dict.get("cover_image", "")
        banner_image = anime_dict.get("banner_image", "")
        airing_format = anime_dict.get("airing_format", "")
        airing_status = anime_dict.get("airing_status", "")
        airing_ep = anime_dict.get("airing_episodes", "")
        season = anime_dict.get("season", "")
        genres = anime_dict.get("genres", [])
        next_airing_ep = anime_dict.get("next_airing_ep", {})
        anime_link = f'https://anilist.co/anime/{anilist.get_anime_id(message_content)}/'

        genres_new = ', '.join(genres)

        try:
            initial_time = next_airing_ep.get('timeUntilAiring', 0)
            mins, secs = divmod(initial_time, 60)
            hours, mins = divmod(mins, 60)
            days, hours = divmod(hours, 24)
            timer = f'{days} days {hours} hours {mins} mins {secs} secs'
            next_ep_num = next_airing_ep.get('episode', 0)
            next_ep_string = f'Episode {next_ep_num} is releasing in {timer}!\n\n[{jap_name} AniList Page]({anime_link})'
        except:
            next_ep_string = f"This anime's release date has not been confirmed!\n\n[{jap_name} AniList Page]({anime_link})"

        anime_embed = discord.Embed(title=jap_name, description=eng_name, color=0xA0DB8E)
        anime_embed.set_image(url=banner_image)
        anime_embed.set_thumbnail(url=cover_image)  

        if desc:
            desc = desc.strip().replace('<br>', '').replace('<i>', '').replace('</i>', '')
            max_words = 200
            if len(desc) > max_words:
                truncated_desc = desc[:max_words] + '...'
                truncated_desc += f'\n[Show more]({anime_link})'    
                anime_embed.add_field(name="Description", value=truncated_desc, inline=False)
            else:
                anime_embed.add_field(name="Description", value=desc, inline=False)

        anime_embed.add_field(name="Airing Date", value=starting_time, inline=True)
        anime_embed.add_field(name="Ending Date", value=ending_time, inline=True)
        anime_embed.add_field(name="Season", value=season, inline=True)

        try:
            episodes = int(airing_ep)
            airing_info = f"{airing_format} ({airing_ep} {'episodes' if episodes > 1 else 'episode'})"
        except:
            airing_info = airing_format

        anime_embed.add_field(name="Airing Format", value=airing_info, inline=True)
        anime_embed.add_field(name="Airing Status", value=airing_status, inline=True)
        anime_embed.add_field(name="Genres", value=genres_new, inline=True)
        anime_embed.add_field(name="Next Episode ~", value=next_ep_string, inline=False)

        await ctx.send(embed=anime_embed)
    except Exception as e:
        send_log_message('error', f"Error creating anime embed: {e}")
        await ctx.send("An error occurred while creating the anime embed.")

@bot.command(name="manga")
async def manga(ctx):
    """Search Manga"""
    message_content = ctx.message.content[len("/manga") + 1:]
    try:
        manga_info = anilist.get_manga(message_content)
    except Exception as e:
        send_log_message('error', f"Error fetching manga: {e}")
        return await ctx.send("Manga not found! Please try again or use a different name. (romaji preferred)")

    try:
        embed = discord.Embed(title=manga_info['name_romaji'], description=manga_info['name_english'], color=0xA0DB8E)
        embed.set_image(url=manga_info['banner_image'])
        embed.set_thumbnail(url=manga_info['cover_image'])

        embed.add_field(name="Starting Time", value=manga_info['starting_time'], inline=True)
        embed.add_field(name="Ending Time", value=manga_info['ending_time'], inline=True)
        embed.add_field(name="Release Format", value=manga_info['release_format'], inline=True)
        embed.add_field(name="Release Status", value=manga_info['release_status'], inline=True)
        
        desc = manga_info['desc']
        if desc:
            desc = desc.strip().replace('<br>', '').replace('<i>', '').replace('</i>', '')
            embed.add_field(name="Description", value=desc, inline=False)

        genres = ', '.join(manga_info['genres'])
        if genres:
            embed.add_field(name="Genres", value=genres, inline=False)

        await ctx.send(embed=embed)
    except Exception as e:
        send_log_message('error', f"Error creating manga embed: {e}")
        await ctx.send("An error occurred while creating the manga embed.")

keep_alive()
bot.run(DISCORD_BOT_TOKEN, log_handler=discord_handler)
