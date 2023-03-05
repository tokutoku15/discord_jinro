import discord
from discord.utils import get
import asyncio
from Manager.Discord.RoleManager import RoleManager
from Manager.Discord.TextChannelManager import TextChannelManager
from Manager.Discord.EmojiManager import EmojiManager
from Manager.Game.GameRuleManager import GameRuleManager
from Manager.Game.GameStateManager import GameStateManager
from Manager.Game.JobManager import JobManager
from Manager.Game.PlayerManger import PlayerManager
from GameMaster.GameMaster import GameMaster

class CommandHandler():
    def __init__(self):
        self.jobManager = JobManager()
        self.roleManager = RoleManager()
        self.textChannelManager = TextChannelManager()
        self.emojiManager = EmojiManager()
        self.gameStateManager = GameStateManager()
        self.gameRuleManager = GameRuleManager()
        self.playerManager = PlayerManager()
        self.GM = GameMaster(self.gameRuleManager, self.gameStateManager, self.jobManager, self.playerManager)
        self.menu_message = None
        self.game_guild = None
        # self.game_guild = discord.Guild()
        self.lobby_channel = None
        self.jinro_channel = None
        self.voice_channel = None

    def link_channels(self, lobby_ch, jinro_ch, voice_ch):
        self.lobby_channel = lobby_ch
        self.jinro_channel = jinro_ch
        self.voice_channel = voice_ch
        self.GM.register_lobby_channel(self.lobby_channel)
    
    def link_info(self, guild):
        self.game_guild = guild
        self.roleManager.register_guild(guild=self.game_guild)
        self.textChannelManager.register_guild(guild=self.game_guild)
        self.emojiManager.register_guild(guild=self.game_guild)
        emoji_list = self.emojiManager.get_emoji_list()
        self.jobManager.register_job_emoji(emoji_list)
    
    async def delete_roles_channels(self):
        await self.roleManager.delete_roles()
        await self.textChannelManager.delete_channels()

    async def join(self, ctx:discord.Interaction):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        role = await self.roleManager.assign_role(ctx.user)
        text, err  = self.playerManager.register_player(ctx.user.name, ctx.user.id, role)
        if err:
            await ctx.response.send_message(text, ephemeral=True)
            return
        await ctx.response.send_message(text)
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        print(self.menu_message)
        await self.menu_message.delete()
        self.menu_message = await self.lobby_channel.send(embed=embed)
        print(self.menu_message)
    
    async def exit(self, ctx:discord.Interaction):
        text = ''
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        text, err = self.playerManager.remove_player(ctx.user.name, ctx.user.id)
        if err:
            await ctx.response.send_message(text, ephemeral=True)
            return
        await self.roleManager.delete_role(ctx.user.name)
        await ctx.response.send_message(text)
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        print(self.menu_message)
        await self.menu_message.delete()
        self.menu_message = await self.lobby_channel.send(embed=embed)
        print(self.menu_message)
    
    async def run(self, ctx:discord.Interaction):
        text = ''
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_sleep(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        self.gameStateManager.active_bot()
        if self.voice_channel.members:
            member_num = len(self.voice_channel.members)
            if  member_num >= 3:
                self.jobManager.set_default_num(member_num)
            for member in self.voice_channel.members:
                role = await self.roleManager.assign_role(member)
                self.playerManager.register_player(member.display_name, member.id, role)
        text = 'botを起動します。おはようございます。\nこれからゲームの設定を始めます。'
        await ctx.response.send_message(text)
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        self.menu_message = await self.lobby_channel.send(embed=embed)
        print(self.menu_message)
    
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
        print(self.menu_message)
    
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
        print(self.menu_message)
    
    async def job(self, ctx:discord.Interaction, name:str, num:int):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        text = '役職の数を変更しました'
        await ctx.response.send_message(text)
        self.jobManager.set_job_num(name, num)
        await self.menu_message.delete()
        embed = self.gameRuleManager.game_setting_Embed(self.jobManager, self.playerManager)
        self.menu_message = await self.lobby_channel.send(embed=embed)
    
    async def help(self, ctx:discord.Interaction):
        text = 'ゲーム設定コマンドを表示します'
        await ctx.response.send_message(text, ephemeral=True)
        embed = self.gameRuleManager.help_command_Embed()
        await ctx.followup.send(embed=embed, ephemeral=True)

    async def start(self, ctx:discord.Interaction):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        if not await self.is_game_ready(ctx):
            return
        if not await self.is_ok_job_count(ctx):
            return
        self.gameStateManager.game_start()
        text = 'ゲームを始めます。'
        await ctx.response.send_message(text)
        self.assign_jobs()
        await self.make_private_channels()
        await self.GM.send_players_job()
        # await asyncio.sleep(3)
        await self.GM.send_night_phase(ctx)

    async def stop(self, ctx:discord.Interaction):
        if not await self.is_lobby_channel(ctx):
            return
        if not await self.is_bot_active(ctx):
            return
        self.playerManager.__init__()
        self.jobManager.__init__()
        self.gameStateManager.game_stop()
        self.gameStateManager.stop_bot()
        self.delete_roles_channels()
        if self.menu_message:
            await self.menu_message.delete()
        text = 'ゲームを終了し、Botを停止します。おやすみなさい。'
        await ctx.response.send_message(text)

    async def action(self, ctx:discord.Interaction, target:str):
        if not self.textChannelManager.is_private_channel(ctx.channel):
            text = 'プライベートチャンネルで実行してください'
            await ctx.response.send_message(text, ephemeral=True)
            return
        if not await self.is_bot_active(ctx):
            return
        if not self.gameStateManager.get_is_game_start():
            text = 'ゲームは始まっていません\n`/start`コマンドでゲームを始めてください。'
            await ctx.response.send_message(text, ephemeral=True)
            return
        s_player = self.playerManager.get_player_from_member(mem_id=ctx.user.id)
        if not s_player.get_is_alive():
            text = '犠牲者はアクションできません。ゲームが終了するまでお待ちください。'
            await ctx.response.send_message(text)
            return
        # @ロール名 で送信すると <@&{ROLE_ID}> になる
        t_player = self.playerManager.get_player_from_role(name=target)
        if t_player is None:
            text = 'プレイヤーを選択してください ex. 「@player-ほげほげ」'
            await ctx.response.send_message(text)
            return
        await self.GM.accept_action(ctx=ctx, target=t_player)
    
    async def vote(self, ctx:discord.Interaction, target:str):
        pass

    async def is_lobby_channel(self, ctx:discord.Interaction) -> bool:
        if self.lobby_channel != ctx.channel:
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
    
    async def is_bot_sleep(self, ctx:discord.Interaction) -> bool:
        if self.gameStateManager.get_is_bot_active():
            text = 'botはすでに立ち上がっています。'
            await ctx.response.send_message(text, ephemeral=True)
            return False
        return True
    
    async def is_game_ready(self, ctx:discord.Interaction) -> bool:
        if self.gameStateManager.get_is_game_start():
            text = 'ゲームはもうすでに始まっています。'
            await ctx.response.send_message(text, ephemeral=True)
            return False
        return True
    
    async def is_ok_job_count(self, ctx:discord.Interaction) -> bool:
        player_num = self.playerManager.get_player_count()
        citizen, werewolf = self.jobManager.get_group_count()
        job_num = citizen + werewolf
        if player_num <= 2:
            text = '3人以上でゲームを始めてください'
            await ctx.response.send_message(text)
            return False
        if werewolf <= 0:
            text = '人狼の数を1以上にしてください'
            await ctx.response.send_message(text)
            return False
        if citizen <= werewolf:
            text = '人狼を市民陣営の合計よりも少なくしてください'
            await ctx.response.send_message(text)
            return False
        if player_num != job_num:
            text = 'プレイヤーの合計と役職の合計が一致しません'
            await ctx.response.send_message(text)
            return False
        return True
    
    async def make_private_channels(self):
        category = get(self.game_guild.categories, name="人狼ゲーム")
        for player in self.playerManager.get_player_list():
            if player.get_job().group == 'werewolf':
                await self.textChannelManager.add_role_to_channel(self.jinro_channel, player.role)
            channel = await self.textChannelManager.create_private_channel(player_name=player.name)
            await channel.edit(category=category)
            player.set_channel(channel)
    
    def assign_jobs(self):
        job_stack = self.jobManager.get_stack()
        for player in self.playerManager.get_player_list():
            player.add_job(job_stack.pop(0))
            print(player.get_job())