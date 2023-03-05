import discord
from discord.utils import get

class TextChannelManager():
    def __init__(self):
        self.game_guild = None
        self.private_channels = []
    # ゲームサーバ登録
    def register_guild(self, guild:discord.Guild):
        self.game_guild = guild
    # プレイヤーごとにプライベートチャンネルを作る
    async def create_private_channel(self, player_name:str) -> discord.TextChannel:
        # 部屋名とロール名を同じにする
        role = get(self.game_guild.roles, name=player_name)
        channel = get(self.game_guild.channels, name=player_name)
        if channel:
            self.private_channels.append(channel)
            return channel
        # 部屋の読み取り権限を変更
        overwrites = {
            self.game_guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        channel = await self.game_guild.create_text_channel(player_name, overwrites=overwrites)
        self.private_channels.append(channel)
        return channel
    # チャンネルのoverwritesにroleを追加する
    async def add_role_to_channel(self, channel:discord.TextChannel, role:discord.Role):
        print(channel.overwrites)
        await channel.set_permissions(role, read_messages=True)
    # チャンネルのoverwritesを初期化する
    def init_channel_overwrite(self, channel:discord.TextChannel):
        pass
    # チャンネルを管理リストから削除
    async def reset_channel_list(self):
        self.private_channels = []
    # チャンネル削除
    async def delete_channels(self):
        for channel in self.game_guild.text_channels:
            print(channel.name)
            if not channel.name.startswith('player-'):
                continue
            await channel.delete()
    # チャンネルがプライベートチャンネルか
    def is_private_channel(self, channel:discord.TextChannel)->bool:
        return channel in self.private_channels