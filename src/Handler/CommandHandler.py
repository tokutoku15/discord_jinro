import discord
from discord import (
    Guild,
    TextChannel,
    VoiceChannel,
    Interaction
)
from Manager.Game.GameRuleManager import GameRuleManager
from Manager.Game.GameStateManager import GameStateManager
from Manager.Game.PlayerManger import PlayerManager
from Manager.Game.MainGame import MainGame
from Manager.Discord.EmojiManager import EmojiManager
from Manager.Discord.RoleManager import RoleManager
from Manager.Discord.TextChannelManager import TextChannelManager

class CommandHandler():
    def __init__(self):
        self.guild:Guild = None
        self.lobby_channel:TextChannel = None
        self.jinro_channel:TextChannel = None
        self.voice_channel:VoiceChannel = None
        self.gameRuleManager = GameRuleManager()
        self.gameStateManager = GameStateManager()
        self.playerManager = PlayerManager()
        self.mainGame = MainGame(self.gameRuleManager, self.gameStateManager, self.playerManager)
        self.setting_menu:discord.Message = None
    # Discordの情報をハンドラにも紐づける
    def link_discord_info(self, guild:Guild, lobby:TextChannel, jinro:TextChannel, voice:VoiceChannel):
        self.guild = guild
        self.lobby_channel = lobby
        self.jinro_channel = jinro
        self.voice_channel = voice
        self.emojiManager = EmojiManager(guild=self.guild)
        self.roleManager = RoleManager(guild=self.guild)
        self.textChannelManager = TextChannelManager(guild=self.guild)
        self.mainGame.register_lobby_channel(lobby)
        emojis = self.emojiManager.get_emoji_list()
        self.gameRuleManager.set_job_emoji(emojis)
        
    # チャンネルとロールの削除(起動時とstop時)
    async def delete_channels_roles(self):
        await self.roleManager.delete_roles()
        await self.textChannelManager.delete_channels()
    # ゲームの設定を始める
    async def game(self, inter:Interaction):
        if not await self.is_lobby_channel(inter):
            return
        if not await self.is_wait_mode(inter):
            return
        await inter.response.defer(thinking=False)
        self.gameStateManager.game_setting()
        text = '今からゲームの設定を始めます。\n「**/menu**」や「**/job**」で設定を変更してください。\n' \
                '「**/join**」でゲームに参加、「**/exit**」でゲームから退出できます。\n' \
                '設定が決まったら「**/start**」でゲームを始めてください。'
        embed = discord.Embed(title="#### Botの起動 ####", description=text, color=0x888888)
        await inter.followup.send(embed=embed)
        if self.voice_channel.members:
            for member in self.voice_channel.members:
                role = await self.roleManager.assign_role(member)
                self.playerManager.register_player(member=member, role=role)
        embed = self.gameRuleManager.game_setting_embed(self.playerManager)
        self.setting_menu = await inter.channel.send(embed=embed)
    # ゲームに参加する
    async def join(self, inter:Interaction):
        if not await self.is_lobby_channel(inter):
            return
        if not await self.is_setting_mode(inter):
            return 
        role = await self.roleManager.assign_role(inter.user)
        text, err = self.playerManager.register_player(inter.user, role)
        if err:
            await self.send_warning(inter,text)
            return
        await inter.response.defer(thinking=False)
        embed = discord.Embed(title=f'{inter.user.name}さんの参加', description=text)
        embed.set_thumbnail(url=inter.user.avatar)
        await inter.followup.send(embed=embed)
        if self.setting_menu:
            embed = self.gameRuleManager.game_setting_embed(self.playerManager)
            await self.setting_menu.delete()
            self.setting_menu = await inter.channel.send(embed=embed)
    # ゲームから退出する
    async def exit(self, inter:Interaction):
        if not await self.is_lobby_channel(inter):
            return
        if not await self.is_setting_mode(inter):
            return
        text, err = self.playerManager.remove_player(inter.user)
        if err:
            await self.send_warning(inter,text)
            return
        await inter.response.defer(thinking=False)
        await self.roleManager.delete_role(inter.user.name)
        await inter.followup.send(text)
        embed = self.gameRuleManager.game_setting_embed(self.playerManager)
        await self.setting_menu.delete()
        self.setting_menu = await self.lobby_channel.send(embed=embed)
    # 第一夜の行動を決める
    async def menu(self, inter:Interaction, menu:str, onoff:str):
        if not await self.is_lobby_channel(inter):
            return
        if not await self.is_setting_mode(inter):
            return
        await inter.response.defer(thinking=False)
        menu_ja = lambda x: '襲撃' if x == 'kill' else '占い'
        text = '第一夜の{}の設定を変更しました。'.format(menu_ja(menu))
        await inter.followup.send(text)
        is_on = lambda x: True if x == 'on' else False
        if menu == 'kill':
            self.gameRuleManager.set_one_night_kill(is_on(onoff))
        else:
            self.gameRuleManager.set_one_night_seer(is_on(onoff))
        embed = self.gameRuleManager.game_setting_embed(self.playerManager)
        await self.setting_menu.delete()
        self.setting_menu = await inter.channel.send(embed=embed)
    # 役職の人数を決める
    async def job(self, inter:Interaction, name:str, num:int):
        if not await self.is_lobby_channel(inter):
            return
        if not await self.is_setting_mode(inter):
            return
        await inter.response.defer(thinking=False)
        text = '役職の数を変更しました'
        await inter.followup.send(text)
        self.gameRuleManager.set_job_num(name, num)
        embed = self.gameRuleManager.game_setting_embed(self.playerManager)
        await self.setting_menu.delete()
        self.setting_menu = await inter.channel.send(embed=embed)
    # ゲームを始める
    async def start(self, inter:Interaction):
        if not await self.is_lobby_channel(inter):
            return
        if not await self.is_setting_mode(inter):
            return
        if not await self.is_ok_job_count(inter):
            return
        await inter.response.defer(thinking=False)
        text = 'ゲームを始めます。'
        await inter.followup.send(text)
        self.assign_jobs()
        await self.make_private_channels()
        # ===========================
        # ここからゲーム本編を始める
        # ===========================
        await self.mainGame.send_players_job()
        await self.mainGame.send_night_phase()
    # ゲームをやめ、botを停止する
    async def stop(self, inter:Interaction):
        if not await self.is_lobby_channel(inter):
            return
        if self.gameStateManager.get_now_phase() == 'wait':
            text = 'botはもう待機状態です。**/game**コマンドでbotを起動してください'
            await self.send_warning(inter,text)
            return
        await inter.response.defer()
        self.mainGame.reset_game()
        self.playerManager.reset_players()
        await self.delete_channels_roles()
        text = 'ゲームを中止し、Botを停止します。おやすみなさい'
        await inter.followup.send(text)
    # 使用できるコマンドを表示する
    async def help(self, inter:Interaction):
        await inter.response.defer(ephemeral=True)
        embed = self.gameRuleManager.bot_command_embed()
        await inter.followup.send(embed=embed)
    # プレイヤーへのアクションを行う
    async def action(self, inter:Interaction, target:str):
        if not await self.is_ok_game_command(inter, "action"):
            return
        # source playerについての処理
        s_player = self.playerManager.get_player_by_member(inter.user)
        if not s_player.is_alive:
            text = '犠牲者はアクションができません。ゲームが終了するまでお待ちください'
            await self.send_warning(inter,text)
            return
        if s_player.has_acted:
            text = 'もうアクションは終えています。他のプレイヤーのアクションが終わるまでお待ちください'
            await self.send_warning(inter,text)
            return
        # target playerについての処理
        t_player = self.playerManager.get_player_by_role(name=target)
        if t_player is None:
            text = 'プレイヤーを選択してください。 ex. 「@player-ほげほげ」'
            await self.send_warning(inter, text)
            return
        await inter.response.defer()
        await self.mainGame.accept_player_action(inter=inter, source=s_player, target=t_player)
    # プレイヤーへの投票を行う
    async def vote(self, inter:Interaction, target:str):
        if not await self.is_ok_game_command(inter, "vote"):
            return
        s_player = self.playerManager.get_player_by_member(inter.user)
        if not s_player.is_alive:
            text = '犠牲者は投票ができません。ゲームが終了するまでお待ちください'
            await self.send_warning(inter,text)
            return
        if s_player.has_acted:
            text = 'もう投票は終えています。他のプレイヤーの投票が終わるまでお待ちください'
            await self.send_warning(inter,text)
            return        
        t_player = self.playerManager.get_player_by_role(name=target)
        if t_player is None:
            text = 'プレイヤーを選択してください。 ex. 「@player-ほげほげ」'
            await self.send_warning(inter, text)
            return
        await inter.response.defer()
        await self.mainGame.accept_player_vote(inter=inter,source=s_player,target=t_player)
    # ロビーチャンネルで実行されてるかどうか
    async def is_lobby_channel(self, inter:Interaction) -> bool:
        if self.lobby_channel != inter.channel:
            text = 'ロビーチャンネルで実行してください'
            await self.send_warning(inter,text)
            return False
        return True
    # botが待機状態か
    async def is_wait_mode(self, inter:Interaction) -> bool:
        if self.gameStateManager.get_now_phase() != 'wait':
            text = 'botが待機状態ではありません'
            await self.send_warning(inter,text)
            return False
        return True
    # botが設定モードか
    async def is_setting_mode(self, inter:Interaction) -> bool:
        if self.gameStateManager.get_now_phase() != 'setting':
            text = 'botが設定モードではありません'
            await self.send_warning(inter,text)
            return False
        return True
    # ジョブの数とプレイヤーの数に相違がないか
    async def is_ok_job_count(self, inter:Interaction) -> bool:
        player_num = self.playerManager.get_player_count()
        citizen, werewolf = self.gameRuleManager.get_group_num()
        job_num = citizen + werewolf
        print(player_num, job_num)
        if player_num <= 2:
            text = '3人以上でゲームを始めてください'
            await self.send_warning(inter,text)
            return False
        if werewolf == 0:
            text = '人狼の数を1以上にしてください'
            await self.send_warning(inter,text)
            return False
        if citizen <= werewolf:
            text = '人狼を市民陣営の合計よりも少なくしてください'
            await self.send_warning(inter,text)
            return False
        if player_num != job_num:
            text = 'プレイヤーの合計と役職の合計が一致しません'
            await self.send_warning(inter,text)
            return False
        return True
    # actionコマンド,voteコマンドを受け付けるためのチェック
    async def is_ok_game_command(self, inter:Interaction, command:str) -> bool:
        if not self.textChannelManager.is_private_channel(inter.channel):
            text = 'プライベートチャンネルでコマンドを実行してください'
            await self.send_warning(inter,text)
            return False
        if self.gameStateManager.get_now_phase() == 'wait':
            text = 'botが待機状態です。**/game**コマンドで起動してください'
            await self.send_warning(inter,text)
            return False
        if self.gameStateManager.get_now_phase() == 'setting':
            text = 'botは設定モードです。**/start**コマンドで起動してください。'
            await self.send_warning(inter,text)
            return False
        if command == 'action' and not self.gameStateManager.get_now_phase() == 'night':
            text = '今はアクションが実行できません。夜の時間に実行してください'
            await self.send_warning(inter,text)
            return False
        elif command == 'vote' and not self.gameStateManager.get_now_phase() == 'vote':
            text = '今は投票できません。投票の時間に実行してください'
            await self.send_warning(inter,text)
            return False
        return True
    # 役職割り当て
    def assign_jobs(self):
        job_stack = self.gameRuleManager.get_job_stack()
        self.playerManager.assign_jobs(job_stack)
    # プライベートチャンネル作成
    async def make_private_channels(self):
        for player in self.playerManager.get_player_list():
            if player.job.appear_group == 'werewolf':
                await self.textChannelManager.add_role_to_channel(self.jinro_channel, player.role)
            channel = await self.textChannelManager.create_private_channel(player_name=player.name)
            player.set_channel(channel)
    # コマンドが実行できないことを送信するメソッド
    async def send_warning(self, inter:Interaction, text:str):
        await inter.response.defer(ephemeral=True)
        await inter.followup.send(text)