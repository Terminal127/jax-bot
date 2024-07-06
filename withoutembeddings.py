from discord.ext import commands
import discord
from discord import Interaction
import requests

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='', intents=intents)

def fetch_anime_data(search_query):
    url = "https://anime-db.p.rapidapi.com/anime"
    querystring = {
        "page": "1",
        "size": "10",
        "search": search_query,
        "genres": "Fantasy,Drama",
        "sortBy": "ranking",
        "sortOrder": "asc"
    }
    headers = {
        "x-rapidapi-key": "API_KEY",
        "x-rapidapi-host": "anime-db.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print(f'Logged in as {bot.user}')
    print(bot.user.id)

@bot.tree.command(name="help", description="This is the help command.")
async def help(interaction: Interaction):
    await interaction.response.send_message("Hello! This is the help command.")

@bot.tree.command(name="ping", description="Ping")
async def ping(interaction: Interaction):
    await interaction.response.send_message("Hello, World! I am just a cute bot.")

@bot.tree.command(name="test", description="just a test code")
async def test(interaction: Interaction):
    await interaction.response.send_message("hello world")

@bot.tree.command(name="anime_search", description="Search for anime")
async def anime_search(interaction: Interaction, query: str):
    """Search for anime using a keyword"""
    await interaction.response.defer()
    data = fetch_anime_data(query)
    
    if not data['data']:
        await interaction.followup.send(f"No results found for '{query}'.")
        return
    
    response = f"Anime Search Results for '{query}':\n\n"
    
    for i, anime in enumerate(data['data'], 1):
        response += (
            f"{i}. {anime['title']}\n"
            f"Type: {anime['type']}\n"
            f"Episodes: {anime['episodes']}\n"
            f"Status: {anime['status']}\n"
            f"Ranking: {anime['ranking']}\n"
            f"Image: {anime['image']}\n"
            f"Genres: {', '.join(anime['genres'])}\n"
            f"More Info: {anime['link']}\n\n"
        )
    
    response += (
        f"Meta Information:\n"
        f"Page: {data['meta']['page']}\n"
        f"Size: {data['meta']['size']}\n"
        f"Total Data: {data['meta']['totalData']}\n"
        f"Total Pages: {data['meta']['totalPage']}"
    )
    
    await interaction.followup.send(response)

# Replace 'TOKEN' with your actual bot token
bot.run("API_KEY")
