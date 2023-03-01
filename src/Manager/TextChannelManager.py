import discord
from discord.utils import get

class TextChannelManager(discord.Client):
    def __init__(self):
        self.game_guild = None
    
    def register_guild(self, guild:discord.Guild):
        self.game_guild = guild

    async def create_private_channel(self, bot_name:str):
        if len(self.game_guild.roles) == 0:
            return
        for role in self.game_guild.roles:
            if not role.name.startswith('player-'):
                continue
            if None != get(self.game_guild.text_channels, name=role.name):
                continue
            # 権限
            overwrites = {
                self.game_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                role: discord.PermissionOverwrite(read_messages=True),
            }
            channel = await self.game_guild.create_text_channel(role.name, overwrites=overwrites)
            self.channels.append(channel)

    async def delete_private_channels(self):
        for channel in self.game_guild.text_channels:
            if channel.name.startswith('player-'):
                await channel.delete()
    
    def is_private_channel(self, channel_name:str):
        if channel_name.startswith('player-'):
            return True
        return False