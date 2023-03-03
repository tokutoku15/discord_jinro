import discord
from Manager.Discord.RoleManager import RoleManager
from Manager.Discord.TextChannelManager import TextChannelManager
from Manager.Game.GameRuleManager import GameRuleManager
from Manager.Game.GameStateManager import GameStateManager
from Manager.Game.JobManager import JobManager
from Manager.Game.PlayerManger import PlayerManager

class CommandHandler():
    def __init__(self):
        self.gameStateManager = GameStateManager()
        self.gameRuleManager = GameRuleManager()
        self.playerManager = PlayerManager()
        self.jobManager = JobManager()
        self.roleManager = RoleManager()
        self.textChannelManager = TextChannelManager()
        self.menu_message = None
        self.lobby_channel = None
        self.jinro_channel = None
        self.voice_channel = None

    def link_channels(self, lobby_ch, jinro_ch, voice_ch):
        self.lobby_channel = lobby_ch
        self.jinro_channel = jinro_ch
        self.voice_channel = voice_ch

    async def join(self, ctx:discord.Interaction):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        text = self.playerManager.register_player(ctx.user.name, ctx.user.id)
        await self.roleManager.create_role(ctx.user)
        await ctx.response.send_message(text)
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        print(self.menu_message)
        await self.menu_message.delete()
        self.menu_message = await self.lobby_channel.send(embed=embed)
    
    async def exit(self, ctx:discord.Interaction):
        text = ''
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        text = self.playerManager.remove_player(ctx.user.name, ctx.user.id)
        await ctx.response.send_message(text)
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        print(self.menu_message)
        await self.menu_message.delete()
        self.menu_message = await self.lobby_channel.send(embed=embed)
    
    async def run(self, ctx:discord.Interaction):
        text = ''
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        self.gameStateManager.active_bot()
        if self.voice_channel.members:
            for member in self.voice_channel.members:
                self.playerManager.register_player(member.name, member.id)
                await self.roleManager.create_role(member)
        text = 'botを起動します。おはようございます。\nゲームの設定を決めてください。'
        await ctx.response.send_message(text)
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        self.menu_message = await self.lobby_channel.send(embed=embed)
    
    async def onenightkill(self, ctx:discord.Interaction, onoff:str):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        text = '第一夜の襲撃の設定を変更しました。'
        await ctx.response.send_message(text)
        await self.menu_message.delete()
        print(onoff)
        is_on = lambda x: True if x == 'on' else False
        self.gameRuleManager.set_one_night_kill(is_on(onoff))
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        self.menu_message = await self.lobby_channel.send(embed=embed)
    
    async def onenightseer(self, ctx:discord.Interaction, onoff:str):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        text = '第一夜の占いの設定を変更しました。'
        await ctx.response.send_message(text)
        await self.menu_message.delete()
        print(onoff)
        is_on = lambda x: True if x == 'on' else False
        self.gameRuleManager.set_one_night_seer(is_on(onoff))
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        self.menu_message = await self.lobby_channel.send(embed=embed)

    async def citizen(self, ctx:discord.Interaction, num:int):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        text = '市民の数を変更しました'
        await ctx.response.send_message(text)
        await self.menu_message.delete()
        self.jobManager.set_job_num(1, num)
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        self.menu_message = await self.lobby_channel.send(embed=embed)
    
    async def werewolf(self, ctx:discord.Interaction, num:int):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        text = '人狼の数を変更しました'
        await ctx.response.send_message(text)
        await self.menu_message.delete()
        self.jobManager.set_job_num(2, num)
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        self.menu_message = await self.lobby_channel.send(embed=embed)

    async def knight(self, ctx:discord.Interaction, num:int):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        text = '騎士の数を変更しました'
        await ctx.response.send_message(text)
        await self.menu_message.delete()
        self.jobManager.set_job_num(3, num)
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        self.menu_message = await self.lobby_channel.send(embed=embed)

    async def seer(self, ctx:discord.Interaction, num:int):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        text = '占い師の数を変更しました'
        await ctx.response.send_message(text)
        await self.menu_message.delete()
        self.jobManager.set_job_num(4, num)
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        self.menu_message = await self.lobby_channel.send(embed=embed)

    async def medium(self, ctx:discord.Interaction, num:int):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        text = '霊媒師の数を変更しました'
        await ctx.response.send_message(text)
        await self.menu_message.delete()
        self.jobManager.set_job_num(5, num)
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        self.menu_message = await self.lobby_channel.send(embed=embed)

    async def start(self, ctx:discord.Interaction):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        self.gameStateManager.game_start()
        await self.menu_message.delete()
        text = 'それではゲームを始めます。'
        await ctx.response.send_message(text)


    async def stop(self, ctx:discord.Interaction):
        pass

    async def ability(self, ctx:discord.Interaction):
        pass

    async def vote(self, ctx:discord.Interaction):
        pass

    async def is_lobby_channel(self, ctx:discord.Interaction) -> bool:
        if not self.lobby_channel == ctx.channel:
            text = 'ロビーチャンネルで実行してください'
            await ctx.response.send_message(text, ephemeral=True)
            return False
        return True
    
    async def is_bot_active(self, ctx:discord.Interaction) -> bool:
        if not self.gameStateManager.get_is_bot_active():
            text = 'botは休止中です。`/run`コマンドで起こしてください。'
            await ctx.response.send_message(text, ephemeral=True)
            return False
        return True
    
    async def is_game_ready(self, ctx:discord.Interaction) -> bool:
        if self.gameStateManager.get_is_game_start():
            text = 'ゲームはもうすでに始まっています。'
            await ctx.response.send_message(text, ephemeral=True)
            return False
        return True