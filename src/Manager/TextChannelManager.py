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
    async def create_private_channel(self, channel_name:str) -> discord.TextChannel:
        # 部屋名とロール名を同じにする
        role = get(self.game_guild.roles, name=channel_name)
        channel = get(self.game_guild.channels, name=channel_name)
        if channel:
            self.private_channels.append(channel)
            return channel
        # 部屋の読み取り権限を変更
        overwrites = {
            self.game_guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        channel = await self.game_guild.create_text_channel(channel_name, overwrites=overwrites)
        self.private_channels.append(channel)
        return channel
    
    def is_private_channel(self, channel):
        if channel in self.private_channels:
            return True
        return False