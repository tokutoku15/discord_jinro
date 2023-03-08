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
message:discord.Message = None
guild:discord.Guild = None
lobby_channel:discord.TextChannel = None
jinro_channel:discord.TextChannel = None
voice_channel:discord.VoiceChannel = None

@tree.command(name='game', description='ゲームの設定を開始する')
@discord.app_commands.guild_only()
async def game(inter:discord.Interaction):
    await cmdHandler.game(inter=inter)

@tree.command(name='join', description='人狼ゲームに参加する(ゲーム開始前)')
@discord.app_commands.guild_only()
async def join(inter:discord.Interaction):
    await cmdHandler.join(inter=inter)

@tree.command(name='exit', description='人狼ゲームから退出する(ゲーム開始前)')
@discord.app_commands.guild_only()
async def exit(inter:discord.Interaction):
    await cmdHandler.exit(inter=inter)

@tree.command(name='menu', description='第一夜の行動の設定')
@discord.app_commands.describe(text="メニューの選択")
@discord.app_commands.rename(text='name')
@discord.app_commands.choices(
    text=[
        discord.app_commands.Choice(name="第一夜の襲撃",value="kill"),
        discord.app_commands.Choice(name="第一夜の占い",value="seer"),
    ]
)
@discord.app_commands.describe(onoff="ありかなしか")
@discord.app_commands.rename(onoff='onoff')
@discord.app_commands.choices(
    onoff=[
        discord.app_commands.Choice(name="あり", value="on"),
        discord.app_commands.Choice(name="なし", value="off"),
    ]
)
@discord.app_commands.guild_only()
async def menu(inter:discord.Interaction, *, text:str, onoff:str):
    await cmdHandler.menu(inter=inter, menu=text, onoff=onoff)

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
        discord.app_commands.Choice(name="狂人",value='madman'),
    ]
)
@discord.app_commands.describe(number="役職の数")
@discord.app_commands.rename(number='number')
@discord.app_commands.guild_only()
async def job(inter:discord.Interaction, *, text:str, number:str):
    try:
        await cmdHandler.job(inter=inter, name=text, num=int(number))
    except:
        await inter.response.send_message('numberには数字を設定してください。', ephemeral=True)

@tree.command(name='start', description='人狼ゲームを始める')
@discord.app_commands.guild_only()
async def start(inter:discord.Interaction):
    await cmdHandler.start(inter=inter)

@tree.command(name='stop', description='人狼GMbotを停止する')
@discord.app_commands.guild_only()
async def stop(inter:discord.Interaction):
    await cmdHandler.stop(inter=inter)

@tree.command(name='action', description='役職の能力を使う(ゲーム中)')
@discord.app_commands.describe(text="能力の使用対象 ex. @player-{hogehoge}")
@discord.app_commands.rename(text='player')
@discord.app_commands.guild_only()
async def action(inter:discord.Interaction, text:str):
    await cmdHandler.action(inter=inter, target=text)

@tree.command(name='vote', description='処刑するプレイヤーに投票する(ゲーム中)')
@discord.app_commands.describe(text="投票の対象 ex. @player-{hogehoge}")
@discord.app_commands.rename(text='player')
@discord.app_commands.guild_only()
async def vote(inter:discord.Interaction, text:str):
    await cmdHandler.vote(inter=inter, target=text)


@tree.command(name='help', description='ゲーム設定のコマンド一覧表示')
@discord.app_commands.guild_only()
async def help(inter:discord.Interaction):
    await cmdHandler.help(inter=inter)

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
    cmdHandler.link_discord_info(
        guild=guild,
        lobby=lobby_channel,
        jinro=jinro_channel,
        voice=voice_channel,
        bot=client,
    )
    await cmdHandler.delete_channels_roles()
    print(client.user.name)
    print(client.user.id)
    print('=================')
    await tree.sync()
    await client.change_presence(activity=discord.Game("人狼ゲーム"))

client.run(TOKEN)