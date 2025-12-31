import os
import discord

TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} онлайн!')
