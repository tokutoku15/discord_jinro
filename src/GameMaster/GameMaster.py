import asyncio
import discord
from discord import ButtonStyle
from Player.Player import Player
from Job.Citizen import Citizen
from Manager.Game.GameRuleManager import GameRuleManager
from Manager.Game.GameStateManager import GameStateManager
from Manager.Game.JobManager import JobManager
from Manager.Game.PlayerManger import PlayerManager

class GameMaster():
    def __init__(self, 
                 gameRuleManager:GameRuleManager, 
                 gameStateManager:GameStateManager, 
                 jobManager:JobManager, 
                 playerManager:PlayerManager
        ):
        self.gameRuleManager = gameRuleManager
        self.gameStateManager = gameStateManager
        self.jobManager = jobManager
        self.playerManager = playerManager
        self.lobby_channel = None
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
    
    def register_lobby_channel(self, channel:discord.TextChannel):
        self.lobby_channel = channel

    async def send_night_phase(self):
        title = f'### {self.gameStateManager.day}日目の夜 ###'
        text = '恐ろしい夜がやってきました。これから夜のアクションを始めます。\n' \
               '**「player-」**から始まるプライベートチャンネルでアクションを実行してください。'
        color = self.colors['night']
        embed = discord.Embed(title=title, description=text, color=color)
        await self.lobby_channel.send(embed=embed)
        await self.send_request_action()
    
    async def send_players_job(self):
        for player in self.playerManager.get_player_list():
            player_job = player.get_job()
            job_text = f'あなたの役職は{player_job}です。{player_job.description_action()}'
            color = self.colors['job'][player_job.group]
            embed = discord.Embed(title=player.name+'さん', description=job_text, color=color)
            print(player.get_job().get_emoji())
            emoji_id = player.get_job().get_emoji().id
            url = 'https://cdn.discordapp.com/emojis/{id}' \
                    .format(id=emoji_id)
            embed.set_thumbnail(url=url)
            await player.get_channel().send(embed=embed)
    
    async def send_request_action(self):
        for player in self.playerManager.get_player_list():
            my_job = player.get_job()
            alive_title, alive_text = self.playerManager.get_alive_display(is_alive=True, my_job=my_job)
            victim_title, victim_text = self.playerManager.get_alive_display(is_alive=False, my_job=my_job)
            embed = discord.Embed(title="アクションの実行", description="temp", color=self.colors['night'])
            embed.add_field(name=alive_title, value=alive_text, inline=True)
            embed.add_field(name=victim_title, value=victim_text, inline=True)
            if not player.get_is_alive():
                continue
            player_job = player.get_job()
            request_text = f'{player_job.request_action()}'
            print(player.get_job().job_name, self.gameStateManager.day)
            if self.gameStateManager.day == 1:
                if player.get_job().job_name == 'medium':
                    request_text += '\n※1日目なので人狼だと思うプレイヤーを選択してください。'
                elif player.get_job().job_name == 'seer' and not self.gameRuleManager.one_night_seer:
                    request_text += '\n※第一夜の占いはなしなので人狼だと思うプレイヤーを選択してください。'
                elif player.get_job().job_name == 'werewolf' and not self.gameRuleManager.one_night_kill:
                    request_text += '\n※第一夜の襲撃はなしなので人狼だと思うプレイヤーを選択してください。'
            embed.description=request_text
            await player.get_channel().send(embed=embed)
    
    async def accept_action(self, ctx:discord.Interaction, source:Player,target:Player, err=None):
        text = ''
        if self.gameStateManager.day == 1:
            if source.get_job().job_name == 'medium':
                text, err = Citizen().action(source, target)
            elif source.get_job().job_name == 'seer' and not self.gameRuleManager.one_night_seer:
                text, err = Citizen().action(source, target)
            elif source.get_job().job_name == 'werewolf' and not self.gameRuleManager.one_night_kill:
                text, err = Citizen().action(source, target)
            else:
                text, err = source.get_job().action(source, target)
            if err:
                await ctx.followup.send(text)
                return
        else:
            text, err = source.get_job().action(source, target)
        if err:
            await ctx.followup.send(text)
            return
        source.acted()
        self.vote_count += 1
        await ctx.followup.send(text)
        print(self.vote_count, self.playerManager.get_alive_player_count())
        if self.vote_count == self.playerManager.get_alive_player_count():
            self.vote_count = 0
            await self.lobby_channel.send(content='全員のアクションが終了しました。')
            await self.send_morning_phase()
    
    async def send_morning_phase(self):
        self.gameStateManager.next_day()
        self.gameStateManager.next_phase()
        title = f'### {self.gameStateManager.day}日目の朝 ###'
        text = '夜が明けました。昨晩襲撃されたプレイヤーは・・・\n'
        players_dict = self.playerManager.night_action()
        try:
            if len(players_dict["kill"]) == 1:
                player.be_victim()
                player = players_dict["kill"][0]
                text += f'> **{player}**\nです。' \
                    '\n{player}はゲームが終わるまでゲームの内容について話すことができません。\n\n'
        except:
            text += 'いませんでした！人狼は襲撃に失敗したようです。\n\n'
        text += 'そして新たに人狼と疑われているプレイヤーは・・・\n'
        try:
            if len(players_dict["doubt"]) >= 1:
                for player in players_dict["doubt"]:
                    text += f'> **{player}** \n'
                text += 'です。'
        except:
            text += 'いませんでした！'
        text += 'これから人狼を探し出すために話し合ってください。\n' \
                f'話し合いの時間は{self.gameRuleManager.discuss_time//60}分です。'
        embed = discord.Embed(title=title, description=text, color=self.colors['morning'])
        await self.lobby_channel.send(embed=embed)
        self.playerManager.reset_players_flags()
        await self.discuss_phase()
    
    async def discuss_phase(self):
        print('discuss_phase')
        await self.display_time_remaining()
    
    async def send_vote_phase(self):
        title = "#### 投票の時間 ####"
        text = '話し合いは終了です。\n陽は暮れて、今日も一人容疑者を処刑する時間が訪れました。\n\n' \
                '**「player-」**から始まるプライベートチャンネルで投票を行なってください。'
        embed = discord.Embed(title=title, description=text, color=self.colors['vote'])
        await self.lobby_channel.send(embed=embed)
        self.gameStateManager.next_phase()
        await self.send_request_vote()
        
    async def send_request_vote(self):
        title = '投票の実行'
        text = '処刑するプレイヤー(生存者)に**/vote**コマンドで投票してください。'
        embed = discord.Embed(title=title, description=text, color=self.colors['vote'])
        alive_title, alive_text = self.playerManager.get_alive_display(True, Citizen())
        embed.add_field(name=alive_title, value=alive_text)
        for player in self.playerManager.get_player_list():
            if player.get_is_alive():
                await player.get_channel().send(embed=embed)
    
    async def accept_vote(self, ctx:discord.Interaction):
        self.vote_count += 1
        if self.vote_count == self.playerManager.get_alive_player_count():
            await self.lobby_channel.send('全員の投票が終了しました。')
            await self.send_judgement()
    
    async def send_judgement(self):
        self.vote_count = 0
        title = '#### 処刑の時間 ####'
        text = '投票が終わり、処刑の時間がやってきました。処刑されるプレイヤーは・・・\n'
        if len(self.playerManager.judgement()) == 1:
            player = self.playerManager.judgement()[0]
            text += f'> {player}\nです。{player}はゲームが終わるまでゲームの内容について話すことができません。'
            player.be_victim()
            self.playerManager.reset_players_flags()
            embed = discord.Embed(title=title, description=text, color=self.colors['judgement'])
            await self.lobby_channel.send(embed=embed)
            self.gameStateManager.next_phase()
            self.gameStateManager.next_day()
            await self.send_night_phase()
            return
        else:
            for player in self.playerManager.judgement():
                text += f'> {player}\n'
            text += 'です。\n最多票が複数名いたので決選投票を行います。\n'\
                    'プライベートチャンネルで決選投票をしてください。'
            embed = discord.Embed(title=title, description=text, color=self.colors['vote'])
            await self.lobby_channel.send(embed=embed)
            self.playerManager.reset_players_flags()
            title, text = self.playerManager.get_judgement_display()
            embed = discord.Embed(title=title, description=text, color=self.colors['vote'])
            for player in self.playerManager.get_player_list():
                if player.get_is_alive():
                    await player.get_channel().send(embed=embed)


    # 時間待機をするプログラム
    async def display_time_remaining(self):
        view = discord.ui.View()
        view.add_item(self.PlusButton(gameRuleManager=self.gameRuleManager))
        view.add_item(self.StopButton(gameRuleManager=self.gameRuleManager))
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
        self.gameStateManager.next_phase()
        self.gameRuleManager.reset_time()
        await self.send_vote_phase()
    
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
    
    class StopButton(discord.ui.Button):
        def __init__(self, *,
                     style: ButtonStyle=ButtonStyle.danger,
                     label: str="Stop",
                     gameRuleManager: GameRuleManager
        ):
            super().__init__(style=style, label=label)
            self.gameRuleManager = gameRuleManager
        
        async def callback(self, inter:discord.Interaction):
            text = '話し合いの時間を終了します'
            self.gameRuleManager.set_time(1)
            await inter.response.send_message(text)