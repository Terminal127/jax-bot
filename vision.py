import discord
from discord.ext import commands
import io
import google.generativeai as genai

genai.configure(api_key="AIzaSyAZ7Z9JMP3FRxkv6LqBaJ92xAl156Y83T4")

generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.attachments and message.attachments[0].content_type.startswith('image'):
        image_data = await message.attachments[0].read()
        await process_image(message.channel, image_data)

    await bot.process_commands(message)

async def process_image(channel, image_data):
    image_part = {"mime_type": "image/jpeg", "data": image_data}

    prompt_parts = [
        f"Find the name of the movie\n",
        image_part,
    ]

    response = model.generate_content(prompt_parts)
    await channel.send(f"AI: {response.text}")

if __name__ == "__main__":
    bot.run("MTE5MTA3Mzk5MTE5NzIwODU5Ng.GoOoNZ.1bz1OXrrKsreOq46O83kQWjjjepFr9sDYfmXSQ")

