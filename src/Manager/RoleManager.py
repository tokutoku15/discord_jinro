import discord
from discord.utils import get

class RoleManager(discord.Client):
    def __init__(self):
        self.color_code = {
            'player_role' : 0xe6e028
        }
        self.game_guild = None
    
    def register_guild(self, guild:discord.Guild):
        self.game_guild = guild
    
    async def create_role(self, player:discord.Member):
        if self.game_guild == None:
            return
        role_name = 'player-'+player.display_name
        if None != get(self.game_guild.roles, name=role_name):
            return
        # discordのロール(権限)を作成
        role = await self.game_guild.create_role(name=role_name)
        # discordのロールを付与
        await player.add_roles(role)
        print(role_name)
    
    async def delete_roles(self):
        if self.game_guild == None:
            print('none')
            return
        for role in self.game_guild.roles:
            if role.name.startswith('player-'):
                await role.delete()