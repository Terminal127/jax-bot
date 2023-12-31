import discord
import os
from dotenv import load_dotenv
# Load environment variables from .env
load_dotenv()

TOKEN = os.environ.get('TOKEN')

# Set your bot token here
if TOKEN is None:
    raise ValueError("Token not found in environment variables.")
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)

