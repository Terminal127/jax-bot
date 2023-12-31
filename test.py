import discord
import os
from dotenv import load_dotenv
import asyncio
import google.generativeai as genai

load_dotenv()

TOKEN = os.environ.get('TOKEN')
GENAI_API_KEY = "AIzaSyAZ7Z9JMP3FRxkv6LqBaJ92xAl156Y83T4"  # Replace with your actual API key

# Set your bot token here
if TOKEN is None:
    raise ValueError("Token not found in environment variables.")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Configuring Generative AI
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
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings
)


async def generate_code(prompt, channel):
    response = model.generate_content([prompt])

    full_text = ""
    for part in response.parts:
        full_text += part.text

    await channel.send(f"AI: {full_text}")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    elif message.content.lower().startswith('$generate'):
        user_input = message.content[len('$generate '):]
        await generate_code(user_input, message.channel)


if __name__ == "__main__":
    client.run(TOKEN)

