import discord
from discord.utils import get

class TextChannelManager():
    def __init__(self):
        self.game_guild = None
        self.private_channels = []
        self.werewolf_channel = None
    # ゲームサーバ登録
    def register_guild(self, guild:discord.Guild):
        self.game_guild = guild
    # プレイヤーごとにプライベートチャンネルを作る
    async def create_private_channel(self, role:discord.Role):
        # 部屋名とロール名を同じにする
        room_name = role.name
        channel = get(self.game_guild.channels, name=room_name)
        if channel:
            self.private_channels.append(channel)
            return
        # 部屋の読み取り権限を変更
        overwrites = {
            self.game_guild.default_role: discord.PermissionOverwrite(read_message=False),
            role: discord.PermissionOverwrite(read_message=True),
        }
        channel = await self.game_guild.create_text_channel(room_name, overwrites=overwrites)
        self.private_channels.append(channel)
    
    def is_private_channel(self, channel):
        if channel in self.private_channels:
            return True
        return False