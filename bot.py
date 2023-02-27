# bot.py
import os
import random

import discord
from dotenv import load_dotenv

# Used to get loading information - Create a .env file with your own attributes
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
OWNER = int(os.getenv('DISCORDBOT_OWNER_ID'))
TRIGGER = "!QUACK"

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
    

    if message.content.upper().startswith(TRIGGER):
        if message.author.id == OWNER:
            await message.reply("Hello Father")
        else:
            await message.reply("Hello World")
        await message.add_reaction()


client.run(TOKEN)
