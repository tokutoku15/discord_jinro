# coding:utf-8
import discord
import discord.app_commands
from discord.utils import get
from Handler.CommandHandler import CommandHandler
from Manager.PlayerManger import PlayerManager
from Manager.RoleManager import RoleManager
from Manager.TextChannelManager import TextChannelManager
from Assets.Button import CreateButton
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
#========== class instance ==============#
cmdHander = CommandHandler()
playerManager = PlayerManager()
roleManager = RoleManager()
textChannelManager = TextChannelManager()
#========= global =============#
message = None
guild = None
text_channel = None
jinro_text_channel = None
voice_channel = None

@tree.command(name='join', description='人狼ゲームに参加する(ゲームが始まる前)')
@discord.app_commands.guild_only()
async def join(ctx:discord.Interaction):
    text, err = cmdHander.join(ctx=ctx)
    if err:
        await ctx.response.send_message(text, ephemeral=True)
        return
    text = playerManager.register_player(ctx.user)
    await roleManager.create_role(ctx.user)
    await ctx.response.send_message(text)

@tree.command(name='exit', description='人狼ゲームから退出する(ゲームが始まる前)')
@discord.app_commands.guild_only()
async def exit(ctx:discord.Interaction):
    text, err = cmdHander.exit(ctx=ctx)
    if err:
        await ctx.response.send_message(text, ephemeral=True)
        return
    text = playerManager.remove_player(ctx.user)
    await ctx.response.send_message(text)

@tree.command(name='run', description='人狼GMbotを起動する')
@discord.app_commands.guild_only()
async def run(ctx:discord.Interaction):
    text, err = cmdHander.run()
    if err:
        await ctx.response.send_message(text, ephemeral=True)
        return
    # voiceチャンネルに人がいるなら参加
    if voice_channel.members:
        for mem in voice_channel.members:
            playerManager.register_player(mem)
            await roleManager.create_role(mem)
    await ctx.response.send_message(text)

@tree.command(name='start', description='人狼ゲームを始める')
@discord.app_commands.guild_only()
async def start(ctx:discord.Interaction):
    text, err = cmdHander.start()
    if err:
        await ctx.response.send_message(text, ephemeral=True)
        return
    # プライベートチャンネルの作成
    player_list = playerManager.get_player_list()
    for player in player_list:
        await textChannelManager.create_private_channel(player.get_name())
    await ctx.response.send_message(text)

@tree.command(name='bye', description='人狼GMbotを停止する')
@discord.app_commands.guild_only()
async def stop(ctx:discord.Interaction):
    text, err = cmdHander.stop()
    if err:
        await ctx.response.send_message(text, ephemeral=True)
        return
    await ctx.response.send_message(text)

@tree.command(name='ability', description='役職の能力を使う')
@discord.app_commands.describe(text="能力の使用対象 ex. @player-{hogehoge}")
@discord.app_commands.rename(text='player')
@discord.app_commands.guild_only()
async def ability(ctx:discord.Interaction, text:str):
    text, err = cmdHander.ability(text)
    if err:
        await ctx.response.send_message(text, ephemeral=True)
        return
    await ctx.response.send_message(text)

@tree.command(name='vote', description='処刑するプレイヤーに投票する')
@discord.app_commands.describe(text="投票の対象 ex. @player-{hogehoge}")
@discord.app_commands.rename(text='player')
@discord.app_commands.guild_only()
async def vote(ctx:discord.Interaction, text:str):
    text, err = cmdHander.vote(text)
    if err:
        await ctx.response.send_message(text, ephemeral=True)
        return
    await ctx.response.send_message(text)

@tree.command(name="button", description="Embedを編集する")
@discord.app_commands.guild_only()
async def button(ctx:discord.Interaction):
    global message
    embed = discord.Embed(title="buttonコマンド", description="ボタン1")
    if message is None:
        message = await text_channel.send(embed=embed,  view=CreateButton())
        await ctx.response.send_message(f'メッセージはボタン1です', ephemeral=True)
        return
    await message.delete()
    message = await text_channel.send(embed=embed,view=CreateButton())
    await ctx.response.send_message(f'メッセージはボタン1です', ephemeral=True)

@client.event
async def on_ready():
    global guild
    global text_channel
    global jinro_text_channel
    global voice_channel
    guild = client.get_guild(GUILD_ID)
    text_channel = client.get_channel(TEXT_CHANNEL_ID)
    jinro_text_channel = client.get_channel(JINRO_CHANNEL_ID)
    voice_channel = client.get_channel(VOICE_CHANNEL_ID)
    roleManager.register_guild(guild)
    textChannelManager.register_guild(guild)
    print(client.user.name)
    print(client.user.id)
    print('=================')
    await tree.sync()
    await client.change_presence(activity=discord.Game("人狼ゲーム"))

client.run(TOKEN)