import discord
from discord import app_commands

f = open('.env', 'r', encoding='UTF-8')
env = f.read().split()[0]
TOKEN = env

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="username",description="自分のユーザー名を確認")
async def username(interaction: discord.Interaction):
    button = discord.ui.Button(label="確認",style=discord.ButtonStyle.primary,custom_id="check")
    view = discord.ui.View()
    view.add_item(button)
    await interaction.response.send_message("自分のユーザー名を確認してみましょう。",view=view)

@client.event
async def on_ready():
    await tree.sync()

#全てのインタラクションを取得
@client.event
async def on_interaction(inter:discord.Interaction):
    try:
        if inter.data['component_type'] == 2:
            await on_button_click(inter)
    except KeyError:
        pass

async def on_button_click(inter:discord.Interaction):
    custom_id = inter.data["custom_id"]#inter.dataからcustom_idを取り出す
    if custom_id == "check":
        embed = discord.Embed(
            title = "あなたのユーザー名",
            description = inter.user.name + "#" + inter.user.discriminator,
            color = 0x0000ff
        )
        await inter.response.send_message(embed=embed,ephemeral=True)#Embedを「これらはあなただけに表示されています」の状態で送信。


client.run(TOKEN)