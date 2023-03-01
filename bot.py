# bot.py
import os
import dbAccess
import botDBCommands

import discord
from dotenv import load_dotenv

# Used to get loading information - Create a .env file with your own attributes
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
OWNER = int(os.getenv('DISCORDBOT_OWNER_ID'))
TRIGGER = os.getenv('TRIGGER')

client = discord.Client()


# returns the username based on a unique user id
async def discord_username(uid):
    user = await client.fetch_user(uid)
    return user


async def parseRequest(message, id):
    return await projects()

#TODO: change element1 to be the username
async def projects():
    dbReturn = dbAccess.ActiveProjects()
    if not dbReturn:
        return "It doesn't look like there's any projects avalible right now"
    returnString = "The following projects are looking for help: \r\n\n"
    for element in dbReturn:
        returnString += element[2] + " created by " + str(element[1]) + "\n"
    returnString += "\n PM them project leader if you're interested"
    return returnString


def offers(uid):
    dbReturn = dbAccess.FindSignUps(uid)
    return dbReturn


def create(uid, pName):
    dbReturn = dbAccess.CreateProject(uid, pName)
    return dbReturn


def join(uid, pName):
    dbReturn = dbAccess.CreateSignUp(uid, pName)
    return dbReturn



# Runs when bot is started
@client.event
async def on_ready():
    print("BOT ONLINE")


# Runs when a message is detected
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.upper().startswith(TRIGGER):
        response = await parseRequest(message.content, message.author.id)
        await message.reply(response)
        # await message.add_reaction()


client.run(TOKEN)

