import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('')
client = discord.Client()

@client.event
async def on_ready():
    print(f"Bot online! {client.user}")

client.run(TOKEN)