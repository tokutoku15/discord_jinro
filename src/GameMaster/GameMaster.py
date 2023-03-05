import discord
from Manager.Game.GameRuleManager import GameRuleManager
from Manager.Game.GameStateManager import GameStateManager
from Manager.Game.JobManager import JobManager
from Manager.Game.PlayerManger import PlayerManager

class GameMaster():
    def __init__(self, gameRuleManager:GameRuleManager, gameStateManager:GameStateManager, jobManager:JobManager, playerManager:PlayerManager):
        self.gameRuleManager = gameRuleManager
        self.gameStateManager = gameStateManager
        self.jobManager = jobManager
        self.playerManager = playerManager
        self.colors = {
            'night' : 0x343D73,
            'morning' : 0xbde3f2,
            'discuss' : 0xbde3f2,
            'vote' : 0xf29944,
        }
    
    async def send_night_phase(self, ctx:discord.Interaction):
        title = f'### {self.gameStateManager.day}日目の夜 ###'
        # title = '### {}{} ###'.format(self.gameStateManager.day, self.gameStateManager.self.game_text['night']['title'])
        text = '恐ろしい夜がやってきました。\nこれから夜のアクションを始めます。\n' \
               '**「player-」**から始まるプライベートチャンネルでアクションを実行してください。'
        color = self.colors['night']
        embed = discord.Embed(title=title, description=text, color=color)
        await ctx.channel.send(embed=embed)
    
    async def send_players_job(self):
        for player in self.playerManager.get_player_list():
            player_job = player.get_job()
            job_text = f'あなたの役職は{player_job}です。{player_job.description_action()}'
            embed = discord.Embed(title=player.name+'さん', description=job_text)
            print(player.get_job().get_emoji())
            emoji_id = player.get_job().get_emoji().id
            url = 'https://cdn.discordapp.com/emojis/{id}' \
                    .format(id=emoji_id)
            embed.set_thumbnail(url=url)
            await player.get_channel().send(embed=embed)