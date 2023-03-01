# bot.py
import os
import dbAccess
import asyncio

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


async def parseRequest(message, uid):
    message = message.replace("[","").replace("]","")
    command = message.split()

    if len(command) == 2 and command[1].upper() == "PROJECTS":
        return await projects()
    elif len(command) == 2 and command[1].upper() == "OFFERS":
        return await offers(uid)
    elif len(command) == 3 and command[1].upper() == "CREATE":
        return await create(uid, command[2])
    elif len(command) == 3 and command[1].upper() == "JOIN":
        return await join(uid, command[2])
    

    elif len(command) == 3 and command[1].upper() == "HELP" and command[2].upper() == "PROJECTS":
        return (f"Usage: \"{TRIGGER} PROJECTS\". Displays a list of all avalible projects looking for help")
    elif len(command) == 3 and command[1].upper() == "HELP" and command[2].upper() == "OFFERS":
        return (f"Usage: \"{TRIGGER} OFFERS\". If you've created a project with me this will tell you all the users who have signed up")
    elif len(command) == 3 and command[1].upper() == "HELP" and command[2].upper() == "CREATE":
        return (f"Usage: \"{TRIGGER} CREATE [project_name]\" note project name must be all 1 word. This will create a new project as you as the owner, If the name is already in use then I will adjust it")
    elif len(command) == 3 and command[1].upper() == "HELP" and command[2].upper() == "JOIN":
        return (f"Usage: \"{TRIGGER} JOIN [project_name]\" note project name must be exact. Will signal you would like to help out with the project")
    

    elif len(command) == 2 and command[1].upper() == "HELP":
        return ("Avalible commands are: [projects], [offers], [create] and [join]. For further info you can type \"!quack help [command]\" ")
    else:
        return ("Sorry that command wasn't found. Try !quack help for how I work")


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

