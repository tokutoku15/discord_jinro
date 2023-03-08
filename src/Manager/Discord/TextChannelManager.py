import discord
from discord.utils import get

class TextChannelManager():
    def __init__(self, guild:discord.Guild=None):
        self.game_guild = guild
        self.private_channels = []
    # プレイヤーごとにプライベートチャンネルを作る
    async def create_private_channel(self, player_name:str) -> discord.TextChannel:
        category = get(self.game_guild.categories, name="人狼ゲーム")
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
        await channel.edit(category=category)
        self.private_channels.append(channel)
        return channel
    # チャンネルのoverwritesにroleを追加する
    async def add_role_to_channel(self, channel:discord.TextChannel, role:discord.Role):
        await channel.set_permissions(role, read_messages=True)
    # チャンネルのoverwritesを初期化する
    async def remove_role_from_channel(self, channel:discord.TextChannel, role:discord.Role):
        await channel.set_permissions(role, read_messages=False)
    # チャンネルを管理リストから削除
    async def reset_channel_list(self):
        self.private_channels = []
    # チャンネル削除
    async def delete_channels(self):
        for channel in self.game_guild.text_channels:
            if not channel.name.startswith('player-'):
                continue
            await channel.delete()
    # チャンネルがプライベートチャンネルか
    def is_private_channel(self, channel:discord.TextChannel)->bool:
        return channel in self.private_channels