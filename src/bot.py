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
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
TIME_FORMAT = os.getenv("TIME_FORMAT")
DATE_FORMAT = os.getenv("DATE_FORMAT")
DATE_RANGE = os.getenv("DATE_RANGE")
USER_RANGE = os.getenv("USER_RANGE")


# Enable the members privileged intent
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)

    print(
        f"{bot.user.name} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})\n"
    )
    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}\n")


@bot.event
async def on_voice_state_update(member, before, after):
    user = member.name

    now = datetime.now()
    current_time = now.strftime(TIME_FORMAT)

    punchin_channel = discord.utils.find(
        lambda g: g.name == PUNCHIN_CHANNEL, bot.get_all_channels()
    )

    sheet = gsheet()

    # Insert today's date if not found
    date_index = sheet.get_today_index(SPREADSHEET_ID)
    if date_index == None:
        today = datetime.today()
        sheet.append_value(
            SPREADSHEET_ID, DATE_RANGE, {"values": [[today.strftime(DATE_FORMAT)]]}
        )

    # Find the cell address to insert current_time
    update_index = sheet.get_update_address(SPREADSHEET_ID, user)
    update_range = f"{update_index}:{update_index}"

    # When user joins the voice channel
    if before.channel == None and after.channel != None:
        await punchin_channel.send(f"{user} joins the Study Room at {current_time}")
        prev_time = sheet.get_value(SPREADSHEET_ID, update_range)
        new_value = (
            current_time if len(prev_time) == 0 else prev_time[0][0] + current_time
        )
        sheet.insert_value(SPREADSHEET_ID, update_range, {"values": [[new_value]]})
    # When user leaves the voice channel
    elif before.channel != None and after.channel == None:
        await punchin_channel.send(f"{user} leaves the Study Room at {current_time}")
        prev_time = sheet.get_value(SPREADSHEET_ID, update_range)
        new_value = f"{prev_time[0][0]} ~ {current_time}\n"
        sheet.insert_value(SPREADSHEET_ID, update_range, {"values": [[new_value]]})


@bot.event
async def on_member_join(member):
    user = member.name
    print(f"{user} joined!\n")
    sheet = gsheet()
    user_arr = sheet.get_value(SPREADSHEET_ID, USER_RANGE)
    user_arr[0].append(user)
    sheet.insert_value(SPREADSHEET_ID, USER_RANGE, {"values": user_arr})


@bot.command(name="echo", help="Use the bot to echo input")
async def echo_input(ctx, arg):
    await ctx.send(f"This is from user {ctx.message.author.name}: {arg}")


@bot.command(name="stop", help="Shutdown the bot")
async def stop_bot(ctx):
    await ctx.send("Stopping the bot...")
    await bot.logout()


@bot.command(name="get_my_study_record", help="Retrieve user's study time record")
async def send_to_google_sheet(ctx):
    user = ctx.author.name
    sheet = gsheet()
    update_index = sheet.get_update_address(SPREADSHEET_ID, user)
    update_range = f"{update_index}:{update_index}"
    record = sheet.get_value(SPREADSHEET_ID, update_range)
    await ctx.send(f"{record[0][0]}" if len(record) != 0 else "No record found")


bot.run(TOKEN)