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

@tree.command(name='help', description='ゲーム設定のコマンド一覧表示')
@discord.app_commands.guild_only()
async def help(ctx:discord.Interaction):
    await cmdHandler.help(ctx=ctx)

@tree.command(name='start', description='人狼ゲームを始める')
@discord.app_commands.guild_only()
async def start(ctx:discord.Interaction):
    await cmdHandler.start(ctx=ctx)

@tree.command(name='stop', description='人狼GMbotを停止する')
@discord.app_commands.guild_only()
async def stop(ctx:discord.Interaction):
    await cmdHandler.stop(ctx=ctx)

@tree.command(name='action', description='役職の能力を使う(ゲーム中)')
@discord.app_commands.describe(text="能力の使用対象 ex. @player-{hogehoge}")
@discord.app_commands.rename(text='player')
@discord.app_commands.guild_only()
async def action(ctx:discord.Interaction, text:str):
    await cmdHandler.action(ctx=ctx, target=text)

@tree.command(name='vote', description='処刑するプレイヤーに投票する(ゲーム中)')
@discord.app_commands.describe(text="投票の対象 ex. @player-{hogehoge}")
@discord.app_commands.rename(text='player')
@discord.app_commands.guild_only()
async def vote(ctx:discord.Interaction, text:str):
    await cmdHandler.vote(ctx=ctx, target=text)

@tree.command(name="job", description="役職の数を変更する")
@discord.app_commands.describe(text="役職名")
@discord.app_commands.rename(text='name')
@discord.app_commands.choices(
    text=[
        discord.app_commands.Choice(name="市民",value="citizen"),
        discord.app_commands.Choice(name="人狼",value="werewolf"),
        discord.app_commands.Choice(name="騎士",value="knight"),
        discord.app_commands.Choice(name="占い師",value="seer"),
        discord.app_commands.Choice(name="霊媒師",value="medium"),
    ]
)
@discord.app_commands.describe(number="役職の数")
@discord.app_commands.rename(number='number')
@discord.app_commands.guild_only()
async def job(ctx:discord.Interaction, *, text:str, number:str):
    try:
        await cmdHandler.job(ctx=ctx, name=text, num=int(number))
    except:
        await ctx.response.send_message('numberには数字を設定してください。', ephemeral=True)

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
    cmdHandler.link_info(guild)
    cmdHandler.link_channels(lobby_channel,jinro_channel,voice_channel)
    await cmdHandler.delete_roles_channels()
    print(client.user.name)
    print(client.user.id)
    print('=================')
    await tree.sync()
    await client.change_presence(activity=discord.Game("人狼ゲーム"))

client.run(TOKEN)