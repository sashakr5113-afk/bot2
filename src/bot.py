import discord
import os

client = discord.Client()
TOKEN = os.getenv('DISCORD_TOKEN')  # Render вставит токен сюда!
client.run(TOKEN)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} онлайн!')  # Обязательно print!

client.run(os.getenv('DISCORD_TOKEN'))
