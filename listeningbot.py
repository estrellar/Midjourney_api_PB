# Discord bot to run continuously and listen for images + upload them?
import discord
import os
import time
import asyncio
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL') 
DIRECTORY = './'

client = discord.Client()

# Keep track of files already seen
seen_files = set(os.listdir('DIRECTORY'))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    while True:
        await check_for_new_files()
        await asyncio.sleep(5)  # wait for 10 seconds

async def check_for_new_files():
    global seen_files
    channel = client.get_channel(CHANNEL_ID)
    files = set(os.listdir(DIRECTORY))
    new_files = files - seen_files
    for file in new_files:
        print(f'Found new file: {file}')
        with open(os.path.join(DIRECTORY, file), 'rb') as f:
            await channel.send(file=discord.File(f))
    seen_files = files

client.run(TOKEN)