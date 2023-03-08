import asyncio
import random
import discord
from discord import Interaction, ButtonStyle
from Player.Player import Player
from Job.Citizen import Citizen
from Manager.Game.GameRuleManager import GameRuleManager
from Manager.Game.GameStateManager import GameStateManager
from Manager.Game.PlayerManger import PlayerManager

class MainGame():
    def __init__(self,
                gameRuleManager:GameRuleManager,
                gameStateManager:GameStateManager,
                playerManager:PlayerManager
    ):
        self.gameRuleManager = gameRuleManager
        self.gameStateManager = gameStateManager
        self.playerManager = playerManager
        self.lobby_channel:discord.TextChannel = None
        self.colors = {
            'night' : 0x444da3,
            'morning' : 0xbde3f2,
            'discuss' : 0xbde3f2,
            'vote' : 0xf29944,
            'job' : {
                'citizen' : 0xfffafa,
                'werewolf' : 0xdc143c,
            },
            'judgement' : 0xdc143c,
            'now' : 0x3c14dc,
        }
        self.vote_count = 0
        self.vote_count_message = []
        self.is_final_vote = False
    def register_lobby_channel(self, channel:discord.TextChannel):
        self.lobby_channel = channel
    def reset_game(self):
        self.vote_count = 0
        self.vote_count_message.clear()
        self.is_final_vote = False
        self.gameStateManager.game_wait()
        self.gameRuleManager.reset_rule()
    # プレイヤーの役職を送信する
    async def send_players_job(self):
        for player in self.playerManager.get_player_list():
            job_text = f'あなたの役職は{player.job}です。{player.job.description_action()}'
            embed = discord.Embed(title=player.name+'さん', description=job_text, color=self.colors['job'][player.job.group])
            emoji_id = player.job.get_emoji().id
            url = f'https://cdn.discordapp.com/emojis/{emoji_id}'
            embed.set_thumbnail(url=url)
            await player.channel.send(embed=embed)
    # 夜のフェーズのテキストを送信する
    async def send_night_phase(self):
        self.gameStateManager.game_start()
        title = f'#### {self.gameStateManager.day}日目の夜 ####'
        text = '恐ろしい夜がやってきました。これから夜のアクションを始めます。\n' \
                '**「player-」**から始まるプライベートチャンネルでアクションを実行してください。'
        embed = discord.Embed(title=title, description=text, color=self.colors['night'])
        await self.lobby_channel.send(embed=embed)
        # await asyncio.sleep(5)
        await self.send_request_action()
    # アクションをリクエストするテキストをそれぞれのチャンネルへ送信
    async def send_request_action(self):
        for player in self.playerManager.get_player_list():
            # 犠牲者は夜のアクションはできないので今の村の状況を送信する
            if not player.is_alive:
                alive_title, alive_text = self.playerManager.get_player_state_display(is_alive=True)
                victim_title, victim_text = self.playerManager.get_player_state_display(is_alive=False)
                text = '現在の村の状況は以下のようになってます。'
                embed = discord.Embed(title="今の村の状況", description=text,color=self.colors['night'])
                embed.add_field(name=alive_title, value=alive_text, inline=True)
                embed.add_field(name=victim_title, value=victim_text, inline=False)
                await player.channel.send(embed=embed)
            # 生存者には今の村の状況と夜のアクションのリクエストを送信する
            else:
                alive_title, alive_text = self.playerManager.get_alive_display(is_alive=True, my_job=player.job)
                victim_title, victim_text = self.playerManager.get_alive_display(is_alive=False, my_job=player.job)
                emoji_id = player.job.get_emoji().id
                url = f'https://cdn.discordapp.com/emojis/{emoji_id}'
                embed = discord.Embed(title="アクションの実行", color=self.colors['night'])
                embed.add_field(name=alive_title, value=alive_text, inline=True)
                embed.add_field(name=victim_title, value=victim_text, inline=True)
                embed.set_thumbnail(url=url)
                request_text = player.job.request_action()
                if self.gameStateManager.day == 1:
                    if player.job.job_name == 'seer' and not self.gameRuleManager.one_night_seer:
                        request_text += '\n※第一夜の占いは「なし」なので人狼だと思うプレイヤーを選択してください。'
                    elif player.job.job_name == 'werewolf' and not self.gameRuleManager.one_night_kill:
                        request_text += '\n※第一夜の襲撃は「なし」なので人狼だと思うプレイヤーを選択してください。'
                else:
                    if player.job.job_name == 'seer' and not self.is_seerable():
                        request_text += '\n※占うことができるプレイヤーはいないので人狼だと思うプレイヤーを選択してください。'
                embed.description = request_text
                await player.channel.send(embed=embed)
    # 占うことができる生存者がいるか
    def is_seerable(self) -> bool:
        for player in self.playerManager.get_player_list():
            if player.is_alive and not player.is_reveal:
                return True
        return False
    # アクションの受付
    async def accept_player_action(self, *, inter:Interaction, source:Player, target:Player, err=None):
        text = ''
        if self.gameStateManager.day == 1:
            if source.job.job_name == 'seer' and not self.gameRuleManager.one_night_seer:
                text, err = Citizen().action(source=source, target=target)
            elif source.job.job_name == 'werewolf' and not self.gameRuleManager.one_night_kill:
                text, err = Citizen().action(source=source, target=target)
            else:
                text, err = source.job.action(source=source, target=target)
            if err:
                await inter.followup.send(text)
                return
        else:
            if source.job.job_name == 'seer' and not self.is_seerable():
                text, err = Citizen().action(source=source, target=target)
            else:
                text, err = source.job.action(source=source, target=target)
        if err:
            await inter.followup.send(text)
            return
        source.finish_act()
        self.vote_count += 1
        await inter.followup.send(text)
        if self.vote_count == self.playerManager.get_alive_player_count():
            self.vote_count = 0
            await self.lobby_channel.send('全員のアクションが終了しました。')
            await self.send_morning_phase()
    # 朝のフェーズを送信
    async def send_morning_phase(self):
        # night -> morning
        self.gameStateManager.next_phase()
        self.gameStateManager.next_day()
        title = f'#### {self.gameStateManager.day}日目の朝 ####'
        text = '夜が明けました。昨晩襲撃されたプレイヤーは・・・\n\n'
        night_action_result = self.playerManager.night_action_result()
        print(night_action_result)
        try:
            player:Player = None
            if len(night_action_result['kill']) == 1:
                player = night_action_result['kill'][0]
            else:
                random.shuffle(night_action_result['kill'])
                player = night_action_result['kill'][0]
            player.fall_victim()
            text += f'> **{player}**\n\nです。\n' \
                    f'{player}はゲームが終わるまでゲームの内容について話すことができません\n\n'
        except:
            text += 'いませんでした！人狼の襲撃は失敗したようです。\n\n'
        text += 'そして新たに人狼と疑われているプレイヤーは・・・\n\n'
        try:
            if len(night_action_result['doubt']) >= 1:
                for player in night_action_result['doubt']:
                    text += f'> **{player}** \n'
                text += '\nです。\n'
            else:
                text += 'いませんでした！'
        except:
            text += 'いませんでした！\n\n'
        text += 'これから人狼を探し出すために話し合いを始めてください\n' \
                f'話し合いの時間は{self.gameRuleManager.discuss_time//60}分です。'
        embed = discord.Embed(title=title, description=text, color=self.colors['morning'])
        await self.lobby_channel.send(embed=embed)
        self.playerManager.reset_players_flags()
        await self.send_discuss_phase()
    # 話し合いのフェーズを送信
    async def send_discuss_phase(self):
        # morning -> discuss
        self.gameStateManager.next_phase()
        await self.display_time_remaining()
    # 話し合いの残り時間を表示
    async def display_time_remaining(self):
        view = discord.ui.View()
        plus_button = self.PlusButton(gameRuleManager=self.gameRuleManager)
        stop_button = self.StopButton(gameRuleManager=self.gameRuleManager, plus_button=plus_button)
        view.add_item(plus_button)
        view.add_item(stop_button)
        print('display_time_remaining')
        minute = self.gameRuleManager.discuss_time // 60
        second = self.gameRuleManager.discuss_time % 60
        text = '**{:02d}分{:02d}秒**'.format(minute, second)
        embed = discord.Embed(title='#### 話し合いの時間 ####', description=text, color=self.colors['discuss'])
        mes = await self.lobby_channel.send(embed=embed, view=view)
        print(mes)
        while self.gameRuleManager.discuss_time > 0:
            self.gameRuleManager.discuss_time -= 1
            minute = self.gameRuleManager.discuss_time // 60
            second = self.gameRuleManager.discuss_time % 60
            text = '**{:02d}分{:02d}秒**'.format(minute, second)
            embed.description = text
            await asyncio.sleep(1)
            await mes.edit(embed=embed)
        # discuss -> vote
        self.gameStateManager.next_phase()
        self.gameRuleManager.reset_time()
        await self.send_vote_phase()
    # 投票フェーズを送信
    async def send_vote_phase(self):
        title = '#### 投票の時間 ####'
        text = '話し合いは終了です。\n陽は暮れて、今日も一人容疑者を処刑する時間が訪れました。\n\n' \
                '**「player-」**から始まるプライベートチャンネルで投票を行なってください。'
        embed = discord.Embed(title=title,description=text, color=self.colors['vote'])
        await self.lobby_channel.send(embed=embed)
        await self.send_request_vote()
    # 投票のリクエストを送信
    async def send_request_vote(self):
        title = '投票の実行'
        text = '処刑するプレイヤー(生存者)に**/vote**コマンドで投票してください'
        embed = discord.Embed(title=title,description=text, color=self.colors['vote'])
        vote_title, vote_text = self.playerManager.get_vote_count_display()
        vote_embed = discord.Embed(title=vote_title, description=vote_text, color=self.colors['vote'])
        for player in self.playerManager.get_player_list():
            if not player.is_alive:
                text += '\n※犠牲者は投票ができません。'
                vote_embed.description = text
            await player.channel.send(embed=embed)
            message = await player.channel.send(embed=vote_embed)
            self.vote_count_message.append(message)
    # プレイヤーの投票を受け付ける
    async def accept_player_vote(self, *, inter:Interaction, source:Player, target:Player):
        text = ''
        if source == target:
            text = '自分に投票することはできません。他のプレイヤーに投票してください。'
            await inter.followup.send(text)
            return
        if not target.is_alive:
            text = '犠牲者に投票することはできません。生存者に投票してください。'
            await inter.followup.send(text)
            return
        target.vote()
        source.finish_act()
        self.vote_count += 1
        text = f'**{target}**に投票しました。他のプレイヤーの投票が終わるまでお待ちください。'
        await inter.followup.send(text)
        vote_title, vote_text = '', ''
        if not self.is_final_vote:
            vote_title, vote_text = self.playerManager.get_vote_count_display()
        else:
            vote_title, vote_text = self.playerManager.get_judgement_display()
        vote_embed = discord.Embed(title=vote_title, description=vote_text, color=self.colors['vote'])
        for mes in self.vote_count_message:
            player = self.playerManager.get_player_by_channel(mes.channel)
            if not player.is_alive:
                vote_text += '\n※犠牲者は投票ができません'
            vote_embed.description = vote_text
            await mes.edit(embed=vote_embed)
        if self.vote_count == self.playerManager.get_alive_player_count():
            self.vote_count = 0
            self.vote_count_message.clear()
            text = '全員の投票が完了しました'
            await self.lobby_channel.send(text)
            await self.send_judgement()
    async def send_judgement(self):
        title = '#### 処刑の時間 ####'
        text = '投票が終わり、処刑の時間がやってきました。処刑されるプレイヤーは・・・\n'
        victims:list = self.playerManager.judgement()
        if len(victims) == 1:
            self.is_final_vote = False
            victim:Player = victims[0]
            text += f'> {victim}\n\nです。{victim}はゲームが終わるまでゲームの内容について話すことはできません。'
            victim.fall_victim()
            print("send_judgement", victim,id(victim))
            self.playerManager.reset_players_flags()
            embed = discord.Embed(title=title, description=text, color=self.colors['judgement'])
            await self.lobby_channel.send(embed=embed)
            self.gameStateManager.next_phase()
            # =========================
            # TODO: 人狼or市民の勝利判定
            # @ここでどちらかが勝利なら終了
            # =========================
            if await self.send_who_win():
                return
            await self.send_night_phase()
            return
        else:
            if not self.is_final_vote:
                self.is_final_vote = True
                for victim in victims:
                    text += f'> {victim}\n'
                text += '\nです。\n最多票が複数名いたので決選投票を行います\n' \
                        'プライベートチャンネルで決選投票をしてください。'
                embed = discord.Embed(title=title, description=text, color=self.colors['judgement'])
                await self.lobby_channel.send(embed=embed)
                self.playerManager.reset_players_flags()
                title, text = self.playerManager.get_judgement_display()
                embed = discord.Embed(title=title, description=text, color=self.colors['vote'])
                for player in self.playerManager.get_player_list():
                    if not player.is_alive:
                        text += '\n※犠牲者は投票ができません。'
                        embed.description = text
                    message = await player.channel.send(embed=embed)
                    self.vote_count_message.append(message)
            else:
                self.is_final_vote = False
                random.shuffle(victims)
                victim = victims[0]
                text += f'> {victim}\n\nです。※再度、最多票が複数名いたためランダムに処刑されます。\n'
                embed = discord.Embed(title=title, description=text, color=self.colors['judgement'])
                victim.fall_victim()
                print("send_judgement", victim,id(victim))
                self.playerManager.reset_judgement()
                self.playerManager.reset_players_flags()
                await self.lobby_channel.send(embed=embed)
                self.gameStateManager.next_phase()
                # =========================
                # TODO: 人狼or市民の勝利判定
                # @ここでどちらかが勝利なら終了
                # =========================
                if await self.send_who_win():
                    return
                await self.send_night_phase()
    # 勝利判定
    async def send_who_win(self, end=False) -> bool:
        alive_citizen, alive_werewolf = self.playerManager.get_alive_appear_group()
        is_knight_alive = self.playerManager.get_is_knight_alive()
        print(alive_citizen, alive_werewolf, is_knight_alive)
        if not is_knight_alive and alive_citizen <= alive_werewolf + 1:
            text = '人狼の勝利'
            await self.lobby_channel.send(text)
            end = True
        elif is_knight_alive and alive_citizen <= alive_werewolf:
            text = '人狼の勝利'
            await self.lobby_channel.send(text)
            end = True
        elif alive_werewolf == 0:
            text = '市民の勝利'
            await self.lobby_channel.send(text)
            end = True
        return end
    # 残り時間を増やすボタン
    class PlusButton(discord.ui.Button):
        def __init__(self, *, 
                    style: ButtonStyle=ButtonStyle.green, 
                    label:str="＋",
                    gameRuleManager: GameRuleManager
        ):
            super().__init__(style=style, label=label)
            self.gameRuleManager = gameRuleManager
        
        async def callback(self, inter:discord.Interaction):
            text = '話し合いの時間を増やしました'
            self.gameRuleManager.add_time(60)
            await inter.response.send_message(text)
    # 話し合いを終了するボタン
    class StopButton(discord.ui.Button):
        def __init__(self, *,
                    style: ButtonStyle=ButtonStyle.danger,
                    label: str="Stop",
                    gameRuleManager: GameRuleManager,
                    plus_button: discord.ui.Button,
        ):
            super().__init__(style=style, label=label)
            self.gameRuleManager = gameRuleManager
            self.plus_button = plus_button
        
        async def callback(self, inter:discord.Interaction):
            text = '話し合いの時間を終了します'
            self.gameRuleManager.set_time(1)
            self.disabled = True
            self.plus_button.disabled = True
            view = discord.ui.View()
            view.add_item(self.plus_button)
            view.add_item(self)
            await inter.response.edit_message(view=view)
            await inter.followup.send(text)