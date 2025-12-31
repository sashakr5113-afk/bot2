import discord

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot("/", intents = intents)

@bot.event
async def on_ready():
    print("Привет, я-бот!")

@bot.event
async def on_message(message):
    if message.content.lower() in ["привет"]:
     await message.channel.send("Привет, мой господин!")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="общий")
    if channel:
        await channel.send(f"Добро пожаловать на сервер, {member.mention}!")

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="общий")
    if channel:
        await channel.send(f"{member.mention} покинул сервер. Пока!")


import aiohttp
import sqlite3

async def check_brave_corp(character_id):
    """Проверяет, в Brave ли персонаж"""
    url = f"https://esi.evetech.net/latest/characters/{character_id}/affiliation/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            alliance_id = data.get('alliance_id')
            # Brave Collective ID: 99005388
            return alliance_id == 99005388

import discord
from discord.ext import commands
import json
import os
import aiohttp

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

AUTH_DATA_FILE = "auth_data.json"

def load_auth_data():
    if os.path.exists(AUTH_DATA_FILE):
        try:
            with open(AUTH_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_auth_data(data):
    try:
        with open(AUTH_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

async def check_brave_corp(character_id):
    try:
        url = f"https://esi.evetech.net/latest/characters/{character_id}/affiliation/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return data.get('alliance_id') == 99005388
    except:
        return False

auth_data = load_auth_data()

@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} готов!")

@bot.command()
async def getroles(ctx):
    user_id = str(ctx.author.id)
    
    if user_id in auth_data:
        user_info = auth_data[user_id]
        
        # ВЫДАЧА РОЛЕЙ
        guild = ctx.guild
        verified_role = discord.utils.get(guild.roles, name="✅ Verified")
        brave_role = discord.utils.get(guild.roles, name="🟢 Brave Pilot")
        
        if verified_role and verified_role not in ctx.author.roles:
            await ctx.author.add_roles(verified_role)
        character_id = user_info.get('character_id')
        is_brave = await check_brave_corp(character_id) if character_id else False
        if brave_role and is_brave and brave_role not in ctx.author.roles:
            await ctx.author.add_roles(brave_role)
        
        embed = discord.Embed(title="✅ Авторизован!", color=0x00ff00)
        embed.add_field(name="Форум", value=user_info.get('username'), inline=True)
        embed.add_field(name="Персонаж", value=user_info.get('character'), inline=True)
        embed.add_field(name="Альянс", value="🟢 Brave" if is_brave else "⚪ Verified", inline=True)
        await ctx.reply(embed=embed)
    else:
        AUTH_URL = "https://account.bravecollective.com/"
        try:
            await ctx.author.send(f"🔗 {AUTH_URL}")
            await ctx.reply("Скинул ссылку в ЛС!")
        except discord.Forbidden:
            await ctx.reply("❌ Открой ЛС!")

@bot.command()
async def test_auth(ctx, username: str, character_id: int):
    user_id = str(ctx.author.id)
    is_brave = await check_brave_corp(character_id)
    
    auth_data[user_id] = {
        "username": username, 
        "character": f"ID: {character_id}",
        "character_id": character_id,
        "is_brave": is_brave
    }
    save_auth_data(auth_data)
    await ctx.reply(f"✅ {ctx.author.mention} → {username} ({'🟢 Brave' if is_brave else '🔴 Не Brave'})")

@bot.command()
async def remove_auth(ctx):
    user_id = str(ctx.author.id)
    if user_id in auth_data:
        del auth_data[user_id]
        save_auth_data(auth_data)
        
        guild = ctx.guild
        verified_role = discord.utils.get(guild.roles, name="✅ Verified")
        brave_role = discord.utils.get(guild.roles, name="🟢 Brave Pilot")
        
        if verified_role and verified_role in ctx.author.roles:
            await ctx.author.remove_roles(verified_role)
        if brave_role and brave_role in ctx.author.roles:
            await ctx.author.remove_roles(brave_role)
        
        await ctx.reply("✅ Данные удалены!")
    else:
        await ctx.reply("❌ Не авторизован.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Ошибка: {error}")





