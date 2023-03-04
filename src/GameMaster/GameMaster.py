import discord
from Manager.Game.GameRuleManager import GameRuleManager
from Manager.Game.GameStateManager import GameStateManager
from Manager.Game.JobManager import JobManager
from Manager.Game.PlayerManger import PlayerManager

class GameMaster():
    def __init__(self, gameRuleManager:GameRuleManager, 
                 gameStateManager:GameStateManager,
                 jobManager:JobManager, 
                 playerManager:PlayerManager):
        self.gameRuleManager = gameRuleManager
        self.gameStateManager = gameStateManager
        self.jobManager = jobManager
        self.playerManager = playerManager
        self.game_text = {
            'night' : {
                'title' : '日目の夜',
                'description' : [ 
                    '恐ろしい夜がやってきました。\nこれから夜のアクションを始めます。\n「player-」から始まるプライベートチャンネルでアクションをしてください。',
                    '容疑者を処刑したにもかかわらず、また'
                ]
            },
            'morning' : {
                'title' : '日目の朝',
                'description' : [
                    '夜が明けました。昨晩襲撃されたプレイヤーは',
                    'です。'
                ]
            }
        }

    async def send_players_job(self):
        for player in self.playerManager.get_player_list():
            await player.get_my_channel().send(f'あなたの役職は{player.get_my_job()}です。')