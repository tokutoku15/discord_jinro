import discord
from Player.Player import Player
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
        self.colors = {
            'night' : 0x343D73,
            'morning' : 0xbde3f2,
            'discuss' : 0xbde3f2,
            'vote' : 0xf29944,
            'job' : {
                'citizen' : 0xfffafa,
                'werewolf' : 0xdc143c,
            },
            'now' : 0x3c14dc,
        }
        self.vote_count = 0
    
    async def send_night_phase(self, ctx:discord.Interaction):
        title = f'### {self.gameStateManager.day}日目の夜 ###'
        text = '恐ろしい夜がやってきました。これから夜のアクションを始めます。\n' \
               '**「player-」**から始まるプライベートチャンネルでアクションを実行してください。'
        color = self.colors['night']
        embed = discord.Embed(title=title, description=text, color=color)
        await ctx.channel.send(embed=embed)
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
            embed.description=request_text
            await player.get_channel().send(embed=embed)
    
    async def accept_action(self, ctx:discord.Interaction, target:Player):
        player = self.playerManager.get_player_from_member(mem_id=ctx.user.id)
        text, err = player.get_job().action(player, target)
        if err:
            await ctx.response.send_message(text)
            return
        self.vote_count += 1
        await ctx.response.send_message(text)