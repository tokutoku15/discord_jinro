import discord
from discord.utils import get

class RoleManager():
    def __init__(self):
        self.game_guild = None
    # ゲームサーバを登録
    def register_guild(self, guild:discord.Guild):
        self.game_guild = guild
    
    async def create_role(self, member:discord.Member) -> discord.Role:
        # ゲームサーバがNoneなら
        if self.game_guild is None:
            print("RoleManager : Game Guile is None")
            return None
        role_name = 'player-'+member.display_name
        role = get(self.game_guild.roles, name=role_name)
        # ロールが存在しているなら
        if role:
            return role
        # ロール(権限)を作成
        role = await self.game_guild.create_role(name=role_name)
        # ロールを付与
        await member.add_roles(role)
        print("add role : ", role_name)
        return role
    
    async def delete_roles(self):
        if self.game_guild is None:
            print("RoleManager : Game Guile is None")
            return
        # ロールを全て削除
        for role in self.game_guild.roles:
            if role.name.startswith('player-'):
                await role.delete()