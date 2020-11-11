import os
import discord
from dotenv import load_dotenv


class MyClient(discord.Client):
    async def on_ready(self):
        guild = discord.utils.find(lambda g: g.name == GUILD, self.guilds)

        print(
            f"{self.user} is connected to the following guild:\n"
            f"{guild.name}(id: {guild.id})\n"
        )
        members = "\n - ".join([member.name for member in guild.members])
        print(f"Guild Members:\n - {members}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == "!stop":
            await message.channel.send("Stopping the bot...")
            await self.logout()

        print("Message from {0.author}: {0.content}".format(message))

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

client = MyClient()
client.run(TOKEN)
