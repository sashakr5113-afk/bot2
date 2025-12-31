import os
import discord

TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("ERROR: DISCORD_TOKEN missing!")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)  # ← Обязательно!

@client.event
async def on_ready():
    print(f'{client.user} онлайн! ID: {client.user.id}')

client.run(TOKEN)
