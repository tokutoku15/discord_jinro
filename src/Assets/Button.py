import discord

class CreateButton(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label="ボタン1")
    async def return_message(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.send_message("折り返しのメッセージ", ephemeral=True)