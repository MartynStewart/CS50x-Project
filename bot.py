# bot.py
import os
import random

import discord
from dotenv import load_dotenv

# Used to get loading information - Create a .env file with your own attributes
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
OWNER = os.getenv('DISCORDBOT_OWNER')

client = discord.Client()

# Runs when bot is started
@client.event
async def on_ready():
    print(f"My Owner is: {OWNER}")
    print("BOT ONLINE")


# Runs when a message is detected
@client.event
async def on_message(message):
    if message.author == client.user:
        # IGNORE SELF MESSAGES
        return

    print(f"New message detected from {message.author}")
    print(f"They have posted: {message.content}")
    
    if message.content == "!Hello":
        if message.author == OWNER:
            await message.reply("Hello Father")
        else:
            await message.reply("Hello World")


client.run(TOKEN)
