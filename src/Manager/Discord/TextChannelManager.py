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
    async def create_private_channel(self, player_name:str) -> discord.TextChannel:
        # 部屋名とロール名を同じにする
        role = get(self.game_guild.roles, name=player_name)
        channel = get(self.game_guild.channels, name=player_name)
        if channel:
            return channel
        # 部屋の読み取り権限を変更
        overwrites = {
            self.game_guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        channel = await self.game_guild.create_text_channel(player_name, overwrites=overwrites)
        self.private_channels.append(channel)
        return channel