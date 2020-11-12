import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
from gsheet import *

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
PUNCHIN_CHANNEL = os.getenv("PUNCHIN_CHANNEL")
SPREADSHEET_ID = "17SRrEAInolD0UxNuzqL_5RVKARzaqKtEXWYnYiU8iiw"
TIME_FORMAT = "%H:%M"


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
    current_time = now.strftime(TIME_FORMAT)

    punchin_channel = discord.utils.find(
        lambda g: g.name == PUNCHIN_CHANNEL, bot.get_all_channels()
    )

    sheet = gsheet()
    # TODO: Insert today's date to the column header
    # date_index = sheet.get_today_index(SPREADSHEET_ID)
    # if (date_index == None):
    #     today = datetime.today()
    #     sheet.add(SPREADSHEET_ID, "A7:A7", {"values": [[today.strftime("%Y-%m-%d")]]})

    # Find the cell address to insert current_time
    user_index = sheet.get_user_index(SPREADSHEET_ID, user)
    date_index = sheet.get_today_index(SPREADSHEET_ID)
    update_index = date_index + str(user_index)
    update_range = f"{update_index}:{update_index}"

    if after.channel != None:
        await punchin_channel.send(f"{user} joins the voice channel at {current_time}")
        prev_time = sheet.get_value(SPREADSHEET_ID, update_range)
        new_value = (
            current_time if len(prev_time) == 0 else prev_time[0][0] + current_time
        )
        sheet.add_value(SPREADSHEET_ID, update_range, {"values": [[new_value]]})
    else:
        await punchin_channel.send(f"{user} leaves the voice channel at {current_time}")
        prev_time = sheet.get_value(SPREADSHEET_ID, update_range)
        new_value = f"{prev_time[0][0]} ~ {current_time}\n"
        sheet.add_value(SPREADSHEET_ID, update_range, {"values": [[new_value]]})


@bot.command(name="echo", help="Use the bot to echo input")
async def echo_input(ctx, arg):
    await ctx.send(f"This is from user {ctx.message.author.name}: {arg}")


@bot.command(name="stop", help="Shutdown the bot")
async def stop_bot(ctx):
    await ctx.send("Stopping the bot...")
    await bot.logout()


@bot.command(name="sheet", help="Send messages to Google Sheet")
async def send_to_google_sheet(ctx, arg):
    await ctx.send(f"Sending {arg} to Google Sheet...")
    sheet = gsheet()
    sheet.add_value(SPREADSHEET_ID, "A3:A3", {"values": [[arg]]})


bot.run(TOKEN)