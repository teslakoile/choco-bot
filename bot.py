import os

import discord
from dotenv import load_dotenv

intents = discord.Intents.default()

intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        await message.reply("Hello! I am Choco1!")


client.run(token)
