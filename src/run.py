# coding:utf-8
import discord
from discord import app_commands
from discord_buttons_plugin import *
from discord.utils import get

# ======== 自作ライブラリ ============ #
from Manager.RoleManager import RoleManager
from Manager.TextChannelManager import TextChannelManager

# ======== .env ========== #
f = open('.env','r', encoding='UTF-8')
env = f.read().split('\n')
ACCESS_TOKEN = env[0]
GUILD_ID = int(env[1])
TEXT_CHANNEL_ID = int(env[2])
VOICE_CHANNEL_ID = int(env[3])
f.close()

# ======== bot ========== #
intents = discord.Intents.all()
client  = discord.Client(intents=intents)
tree    = app_commands.CommandTree(client)
# ===== global ========= #
guild   = None
voice_channel = None
text_channel = None

# ======= 外部クラス群 ========= #
roleManager = RoleManager()
textChannelManager = TextChannelManager()

@tree.command(
        name="data",
        description="Preview discord data"
)
@discord.app_commands.guild_only()
async def data(ctx:discord.Interaction):
    print("members = ", ctx.guild.members)
    print()
    print(ctx.guild.roles)
    print()
    print(ctx.guild.emojis)
    print()
    print(ctx.guild.voice_channels)
    print()
    print(ctx.guild.text_channels)
    await ctx.response.send_message('dataが表示されました',ephemeral=True)

@tree.command(
        name = "setup",
        description="人狼Botの設定を始める"
)
@discord.app_commands.guild_only()
async def setup(ctx:discord.Interaction):
    global text_channel
    global voice_channel
    if ctx.channel != text_channel:
        await ctx.response.send_message('人狼チャンネルでsetupコマンドを使用してください', ephemeral=True)
        return
    # メンバー毎にRole(権限)を付与
    for mem in voice_channel.members:
        await roleManager.create_role(mem)
    embed = discord.Embed(title="setupコマンド", description="ロール付与が終わりました\n/startコマンドでゲームを始めてください")
    await ctx.response.send_message(embed=embed)

@tree.command(
        name = "join",
        description="人狼ゲームに参加する"
)
@discord.app_commands.guild_only()
async def join(ctx:discord.Interaction):
    mem = ctx.message.author
    await roleManager.create_role(mem)
    print(f'join {mem.name}')

@tree.command(
        name = "start",
        description="人狼ゲームを始める"
)
@discord.app_commands.guild_only()
async def start(ctx:discord.Interaction):
    await textChannelManager.create_private_channel(client.user.name)

@tree.command(
        name = "stop",
        description="人狼Botを終了させる"
)
@discord.app_commands.guild_only()
async def stop(ctx:discord.Interaction):
    print('stop')
    embed = discord.Embed(title="stopコマンド", description="stopコマンドが実行されました。\nおやすみなさい。")
    await ctx.response.send_message(embed=embed)

@tree.command(
        name = "delete",
        description="プライベートチャンネルとロールを削除する"
)
@discord.app_commands.guild_only()
async def delete(ctx:discord.Interaction):
    await textChannelManager.delete_private_channels()
    await roleManager.delete_roles()
    await ctx.response.send_message('ロールとテキストチャンネルが削除されました')


# async def vote(ctx:discord.Interaction, subject:str):
#     if text_channel == None:
#         print('None')
#         return
#     ch_name = ctx.message.channel.name
#     if not textChannelManager.is_private_channel(ch_name):
#         await ctx.send('ここでは投票できません。プライベートチャンネルで投票してください')
#         return
#     if not subject:
#         await ctx.send('投票先を/vote の後ろに記入してください')
#         return
#     player_name = ctx.message.author.name
#     player_icon = ctx.message.author.avatar
#     embed = discord.Embed(title="投票", description=f'{subject}に投票しました')
#     embed.set_author(name=player_name,icon_url=player_icon)
#     print(player_icon)
#     await text_channel.send(embed=embed)

# @client.command()
# async def button(ctx):
#     await buttons.send(
#         "テストボタン",
#         channel=ctx.channel.id,
#         components=[
#             ActionRow([
#                 Button(
#                     label="ボタン",
#                     style=ButtonType().Primary,
#                     custom_id="button_clicked",
#                     disabled=False
#                 )
#             ])
#         ]
#     )

# @buttons.click
# async def button_clicked(ctx):
#     print("push button")
#     await ctx.reply("ボタンが押されました", flags=MessageFlags().EPHEMERAL)
#     await ctx.channel.send("ボタンが押されました")

@client.event
async def on_ready():
    # サーバをそれぞれのManagerに登録
    global guild 
    global text_channel
    global voice_channel
    guild = client.get_guild(GUILD_ID)
    text_channel = client.get_channel(TEXT_CHANNEL_ID)
    voice_channel = client.get_channel(VOICE_CHANNEL_ID)
    roleManager.register_guild(guild)
    textChannelManager.register_guild(guild)
    print('We have logged in as {0.user}'.format(client))
    print(client.user.name)
    print(client.user.id)
    print('--------------')
    await tree.sync()
    await client.change_presence(activity=discord.Game("人狼ゲーム"))

client.run(ACCESS_TOKEN)