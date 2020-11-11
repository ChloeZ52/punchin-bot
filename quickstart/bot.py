import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
PUNCHIN_CHANNEL = os.getenv("PUNCHIN_CHANNEL")

bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)

    print(
        f"{bot.user.name} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})\n"
    )
    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}")


@bot.event
async def on_voice_state_update(member, before, after):
    user = member.name
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    punchin_channel = discord.utils.find(
        lambda g: g.name == PUNCHIN_CHANNEL, bot.get_all_channels()
    )
    if after.channel != None:
        await punchin_channel.send(f"{user} joins the voice channel at {current_time}")
    else:
        await punchin_channel.send(f"{user} leaves the voice channel at {current_time}")


@bot.command(name="echo", help="Use the bot to echo input")
async def echo_input(ctx, arg):
    await ctx.send(f"This is from user {ctx.message.author.name}: {arg}")


@bot.command(name="stop", help="Shutdown the bot")
async def stop_bot(ctx):
    await ctx.send("Stopping the bot...")
    await bot.logout()


bot.run(TOKEN)