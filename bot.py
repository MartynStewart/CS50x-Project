# bot.py
import os
import dbAccess
import asyncio

import discord
from dotenv import load_dotenv

# Used to get loading information - Create a .env file with your own attributes
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TRIGGER = os.getenv('TRIGGER')

client = discord.Client()


# returns the username based on a unique user id
async def discord_username(uid):
    user = await client.fetch_user(uid)
    return user


async def parseRequest(message, uid):
    command = message.replace("[","").replace("]","").split()
    length = len(command)
    if(length == 1):
        return("QUACK!")

    userCommand = command[1].upper()
    if userCommand == "HELP":
        return await helpCommands(command)
    if length == 2:
        if userCommand == "PROJECTS":
            return await projects()
        elif userCommand == "OFFERS":
            return await offers(uid)
        else:
            return ("Sorry that command wasn't found. Try !quack help for how I work")
    if length == 3:
        if userCommand == "CREATE":
            return await create(uid, command[2])
        elif userCommand == "JOIN":
            return await join(uid, command[2])
        elif userCommand == "DELETEPROJECT":
            return await deleteProject(uid, command[2])
        elif userCommand == "DELETEOFFER":
            return await deleteOffer(uid, command[2])
        else:
            return ("Sorry that command wasn't found. Try !quack help for how I work")
    return ("Sorry that command wasn't found. Try !quack help for how I work")

async def helpCommands(command):
    if len(command) == 3:
        userCommand = command[2].upper()
        if userCommand == "PROJECTS":
            return (f"Usage: \"{TRIGGER} PROJECTS\". Displays a list of all avalible projects looking for help")
        elif userCommand == "OFFERS":
            return (f"Usage: \"{TRIGGER} OFFERS\". If you've created a project with me this will tell you all the users who have signed up")
        elif userCommand == "CREATE":
            return (f"Usage: \"{TRIGGER} CREATE [project_name]\" note project name must be all 1 word. This will create a new project as you as the owner, If the name is already in use then I will adjust it")
        elif userCommand == "JOIN":
            return (f"Usage: \"{TRIGGER} JOIN [project_name]\" note project name must be exact. Will signal you would like to help out with the project")
        elif userCommand == "DELETEPROJECT":
            return (f"Usage: \"{TRIGGER} DELETEPROJECT [project_name]\" Deletes this project and all sign ups. Note project name must be exact and you must be the creator.")
        elif userCommand == "DELETEOFFER":
            return (f"Usage: \"{TRIGGER} DELETEOFFER [project_name]\" Deletes your sign up for this project. Note project name must be exact].")
        else:
            return ("Avalible commands are: [projects], [offers], [create], [join], [deleteProject] and [deleteOffer]. For further info you can type \"!quack help [command]\" ")
    else:
        return ("Avalible commands are: [projects], [offers], [create], [join], [deleteProject] and [deleteOffer]. For further info you can type \"!quack help [command]\" ")


async def projects():
    dbReturn = dbAccess.ActiveProjects()
    if not dbReturn:
        return "It doesn't look like there's any projects avalible right now"
    returnString = "The following projects are looking for help: \r\n\n"
    for element in dbReturn:
        uName = await discord_username(element[1])
        returnString += str(element[2]) + " created by " + str(uName) + "\n"
    returnString += "\n PM the project leader if you're interested"
    return returnString


async def offers(uid):
    dbReturn = dbAccess.FindSignUps(uid)
    if not dbReturn:
        return "Sorry there's been no sign ups to your project(s) yet"
    returnString = ""
    for element in dbReturn:
        uName = await discord_username(element[0])
        returnString += f"{uName} is willing to help with {element[1]}"
    return returnString


async def create(uid, pName):
    dbReturn = dbAccess.CreateProject(uid, pName)
    return dbReturn


async def join(uid, pName):
    dbReturn = dbAccess.CreateSignUp(uid, pName)
    if(dbReturn):
        return "Successfully joined the project"
    return "Sorry that project was not found. Please check you are spelling the full project name correctly"

async def deleteProject(uid, pName):
    dbReturn = dbAccess.DeleteProject(uid, pName)
    if(dbReturn):
        return "Successfully deleted the project"
    return "Sorry that project was not found under your ID. Please check you are spelling the full project name correctly"

async def deleteOffer(uid, pName):
    dbReturn = dbAccess.DeleteOffer(uid, pName)
    if(dbReturn):
        return "Successfully removed your offer on that project"
    return "Sorry a project offer was not found under your ID. Please check you are spelling the full project name correctly"

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

