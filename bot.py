# bot.py
import os
import dbAccess

import discord
from dotenv import load_dotenv

# Used to get loading information - Create a .env file with your own attributes
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
OWNER = int(os.getenv('DISCORDBOT_OWNER_ID'))
TRIGGER = "!QUACK"

client = discord.Client()


# returns the username based on a unique user id
async def discord_username(uid):
    #return user name from id
    user = await client.fetch_user(uid)
    return user


def parseRequest(message, id):
    return dbAccess.ActiveProjects()


# Runs when bot is started
@client.event
async def on_ready():
    print(f"My Owner is: {OWNER}")
    print(f"My owner is: {await discord_username(OWNER)}")
    print("BOT ONLINE")


# Runs when a message is detected
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.upper().startswith(TRIGGER):
        discord_username(message.author.id)
        if message.author.id == OWNER:
            response = parseRequest(message.content, message.author.id)
            await message.reply(response)
        else:
            response = parseRequest(message.content)
            await message.reply(response)
        await message.add_reaction()


client.run(TOKEN)

