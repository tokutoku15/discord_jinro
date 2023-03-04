# coding:utf-8
import discord
import discord.app_commands
from discord.utils import get
from Handler.CommandHandler import CommandHandler
#======== file read ============#
f = open('.env', 'r', encoding='UTF-8')
env = f.read().split()
TOKEN = env[0]
GUILD_ID = int(env[1])
TEXT_CHANNEL_ID = int(env[2])
VOICE_CHANNEL_ID = int(env[3])
JINRO_CHANNEL_ID = int(env[4])
f.close()
#========= discord ==============#
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
#======== class instances =========#
cmdHandler = CommandHandler()
#========= global =============#
message = None
guild = None
lobby_channel = None
jinro_channel = None
voice_channel = None

@tree.command(name='join', description='人狼ゲームに参加する(ゲーム開始前)')
@discord.app_commands.guild_only()
async def join(ctx:discord.Interaction):
    await cmdHandler.join(ctx=ctx)

@tree.command(name='exit', description='人狼ゲームから退出する(ゲーム開始前)')
@discord.app_commands.guild_only()
async def exit(ctx:discord.Interaction):
    await cmdHandler.exit(ctx=ctx)

@tree.command(name='run', description='人狼GMbotを起動する')
@discord.app_commands.guild_only()
async def run(ctx:discord.Interaction):
    await cmdHandler.run(ctx=ctx)

#============= Game Setting Commands ======================
@tree.command(name='onenightkill', description='第一夜の襲撃の設定')
@discord.app_commands.describe(text="ありかなしか")
@discord.app_commands.rename(text='onoff')
@discord.app_commands.choices(
    text=[
        discord.app_commands.Choice(name="あり",value="on"),
        discord.app_commands.Choice(name="なし",value="off"),
    ]
)
@discord.app_commands.guild_only()
async def onenightkill(ctx:discord.Interaction, text:str):
    await cmdHandler.onenightkill(ctx=ctx, onoff=text)

@tree.command(name='onenightseer', description='第一夜の占いの設定')
@discord.app_commands.describe(text="ありかなしか")
@discord.app_commands.rename(text='onoff')
@discord.app_commands.choices(
    text=[
        discord.app_commands.Choice(name="あり",value="on"),
        discord.app_commands.Choice(name="なし",value="off"),
    ]
)
@discord.app_commands.guild_only()
async def onenightseer(ctx:discord.Interaction, text:str):
    await cmdHandler.onenightseer(ctx=ctx, onoff=text)

@tree.command(name='citizen', description='市民の数を決める')
@discord.app_commands.describe(text="市民の数")
@discord.app_commands.rename(text='number')
@discord.app_commands.guild_only()
async def citizen(ctx:discord.Interaction, text:str):
    try:
        await cmdHandler.citizen(ctx=ctx, num=int(text))
    except:
        await ctx.response.send_message('数字を設定してください。', ephemeral=True)

@tree.command(name='werewolf', description='人狼の数を決める')
@discord.app_commands.describe(text="人狼の数")
@discord.app_commands.rename(text='number')
@discord.app_commands.guild_only()
async def werewolf(ctx:discord.Interaction, text:str):
    try:
        await cmdHandler.werewolf(ctx=ctx, num=int(text))
    except:
        await ctx.response.send_message('数字を設定してください。', ephemeral=True)

@tree.command(name='knight', description='騎士の数を決める')
@discord.app_commands.describe(text="騎士の数")
@discord.app_commands.rename(text='number')
@discord.app_commands.choices(
    text=[
        discord.app_commands.Choice(name="1",value="1"),
        discord.app_commands.Choice(name="0",value="0"),
    ]
)
@discord.app_commands.guild_only()
async def knight(ctx:discord.Interaction, text:str):
    await cmdHandler.knight(ctx=ctx, num=int(text))

@tree.command(name='seer', description='占い師の数を決める')
@discord.app_commands.describe(text="占い師の数")
@discord.app_commands.rename(text='number')
@discord.app_commands.choices(
    text=[
        discord.app_commands.Choice(name="1",value="1"),
        discord.app_commands.Choice(name="0",value="0"),
    ]
)
@discord.app_commands.guild_only()
async def seer(ctx:discord.Interaction, text:str):
    await cmdHandler.seer(ctx=ctx, num=int(text))

@tree.command(name='medium', description='霊媒師の数を決める')
@discord.app_commands.describe(text="霊媒師の数")
@discord.app_commands.rename(text='number')
@discord.app_commands.choices(
    text=[
        discord.app_commands.Choice(name="1",value="1"),
        discord.app_commands.Choice(name="0",value="0"),
    ]
)
@discord.app_commands.guild_only()
async def medium(ctx:discord.Interaction, text:str):
    await cmdHandler.medium(ctx=ctx, num=int(text))

@tree.command(name='help', description='ゲーム設定のコマンド一覧表示')
@discord.app_commands.guild_only()
async def help(ctx:discord.Interaction):
    await cmdHandler.help(ctx=ctx)
#==========================================================

@tree.command(name='start', description='人狼ゲームを始める')
@discord.app_commands.guild_only()
async def start(ctx:discord.Interaction):
    await cmdHandler.start(ctx=ctx)

@tree.command(name='stop', description='人狼GMbotを停止する')
@discord.app_commands.guild_only()
async def stop(ctx:discord.Interaction):
    await cmdHandler.stop(ctx=ctx)

@tree.command(name='ability', description='役職の能力を使う(ゲーム中)')
@discord.app_commands.describe(text="能力の使用対象 ex. @player-{hogehoge}")
@discord.app_commands.rename(text='player')
@discord.app_commands.guild_only()
async def ability(ctx:discord.Interaction, text:str):
    await cmdHandler.ability(ctx=ctx, target=text)

@tree.command(name='vote', description='処刑するプレイヤーに投票する(ゲーム中)')
@discord.app_commands.describe(text="投票の対象 ex. @player-{hogehoge}")
@discord.app_commands.rename(text='player')
@discord.app_commands.guild_only()
async def vote(ctx:discord.Interaction, text:str):
    await cmdHandler.vote(ctx=ctx, target=text)

@tree.command(name="button", description="Embedを編集する")
@discord.app_commands.guild_only()
async def button(ctx:discord.Interaction):
    pass

@client.event
async def on_ready():
    global guild
    global lobby_channel
    global jinro_channel
    global voice_channel
    guild = client.get_guild(GUILD_ID)
    lobby_channel = client.get_channel(TEXT_CHANNEL_ID)
    jinro_channel = client.get_channel(JINRO_CHANNEL_ID)
    voice_channel = client.get_channel(VOICE_CHANNEL_ID)
    cmdHandler.link_guild(guild)
    cmdHandler.link_channels(lobby_channel,jinro_channel,voice_channel)
    print(client.user.name)
    print(client.user.id)
    print('=================')
    await tree.sync()
    await client.change_presence(activity=discord.Game("人狼ゲーム"))

client.run(TOKEN)