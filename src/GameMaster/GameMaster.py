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
        self.victims = []
        self.game_text = {
            'night' : {
                'title' : '日目の夜',
                'description' : {
                    'come' : '恐ろしい夜がやってきました。\nこれから夜のアクションを始めます。\n**「player-」**から始まるプライベートチャンネルでアクションを実行してください。',
                    'continue' : '容疑者を処刑したにもかかわらず、また',
                },
                'color' : 0x343D73
            },
            'morning' : {
                'title' : '日目の朝',
                'description' : {
                    'come' : '夜が明けました。昨晩襲撃されたプレイヤーは',
                    'noone' : 'いませんでした！人狼の襲撃は失敗したようです。',
                    'someone' : 'です。',
                },
                'color' : 0xBDE3F2 
            },
            'discuss' : {
                'title' : '話し合いの時間',
                'description' : {
                    'come' : '話し合いの時間です。'
                }
            }
        }

    async def send_night_embed(self):
        title = '### {}{} ###'.format(self.gameStateManager.day, self.gameStateManager.self.game_text['night']['title'])
        text = '{}'.format(self.game_text['night']['description']['come'])
        if self.gameStateManager.day == 1:
            text = '{}'.format(self.game_text['night']['desciption']['continue']) \
                    + text
        color = self.game_text['night']['color']
        embed = discord.Embed(title=title, description=text, color=color)


    async def send_players_job(self):
        for player in self.playerManager.get_player_list():
            player_job = player.get_job()
            job_text = f'あなたの役職は{player_job}です。{player_job.description_ability()}'
            embed = discord.Embed(title=player.name+'さん', description=job_text)
            emoji_id = player.get_job().get_emoji().id
            url = 'https://cdn.discordapp.com/emojis/{id}' \
                    .format(id=emoji_id)
            embed.set_thumbnail(url=url)
            await player.get_channel().send(embed=embed)