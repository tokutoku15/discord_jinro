# coding:utf-8
import discord
from discord import app_commands
from discord_buttons_plugin import *
from discord.utils import get

f = open('.env', 'r', encoding='UTF-8')
ACCESS_TOKEN = f.read()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(
    name = "",
    description="Send Hello World."
)
@discord.app_commands.describe(
    text = "Text to say hello"
)
@discord.app_commands.rename(
    text="name"
)
@discord.app_commands.guild_only()
async def hoge(ctx:discord.Interaction, text:str):
    print('command hoge run')
    await ctx.response.send_message(f"Hello!")

@client.event
async def on_ready():
    print("ready")
    await tree.sync()

client.run(ACCESS_TOKEN)