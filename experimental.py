import discord
import os
from dotenv import load_dotenv
import requests
import json
import random
import google.generativeai as genai
import asyncio

# indentify intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')
GENAI_API_KEY = os.environ.get('GENAI_API_KEY')

# configure generative AI
genai.configure(api_key=GENAI_API_KEY)

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings
)

model_vision = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)


# define encouragements

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]
starter_encouragements = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person!"
]

# define functions

async def generate_code(prompt, channel):
    response = model.generate_content([prompt])

    full_text = ""
    for part in response.parts:
        full_text += part.text

    await channel.send(f"AI: {full_text}")

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

async def process_image_information(channel, image_data):
    image_part = {"mime_type": "image/jpeg", "data": image_data}
    prompt_parts = [
        f"Find information about this image\n",
        image_part,
    ]
    response = model_vision.generate_content(prompt_parts)
    await channel.send(f"AI: {response.text}")

async def process_image_anime(channel, image_data):
    image_part = {"mime_type": "image/jpeg", "data": image_data}

    prompt_parts = [
        f"Find the name of the anime and info about it in less than 500 characters\n",
        image_part,
    ]

    response = model_vision.generate_content(prompt_parts)
    await channel.send(f"AI: {response.text}")

async def process_image_answer(channel, image_data):
    image_part = {"mime_type": "image/jpeg", "data": image_data}

    prompt_parts = [
        f"Give the answer of the question\n",
        image_part,
    ]

    response = model_vision.generate_content(prompt_parts)
    await channel.send(f"AI: {response.text}")

# define events

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    elif message.content.startswith('jarvis'):
        await message.channel.send('Hello!')
    
    elif message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    
    elif any(word in message.content for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))
    
    elif message.content.startswith('$generate'):
        await message.channel.send('Switched to text based ai')
        user_input = message.content[len('$generate'):]
        await generate_code(user_input, message.channel)

    if message.attachments and message.attachments[0].content_type.startswith('image'):
        if message.content.startswith('$anime'):
            await message.channel.send('Switched to anime based ai')
            image_data = await message.attachments[0].read()
            await process_image_anime(message.channel, image_data)
        elif message.content.startswith('$answer'):
            await message.channel.send('Switched to answer based ai')
            image_data = await message.attachments[0].read()
            await process_image_answer(message.channel, image_data)
        else:
            await message.channel.send('Switched to information based ai')
            image_data = await message.attachments[0].read()
            await process_image_information(message.channel, image_data)


# run client

client.run(TOKEN)
