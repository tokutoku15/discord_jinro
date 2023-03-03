import discord
from discord import Interaction, ButtonStyle
from Manager.Game.JobManager import JobManager
from Manager.Game.PlayerManger import PlayerManager

class GameRuleManager():
    def __init__(self):
        self.one_night_kill = False
        self.one_night_seer = False
        self.discuss_time = 5

    def game_setting_Embed(self, jobManager:JobManager, playerManager:PlayerManager) -> discord.Embed:
        embed = discord.Embed(title="人狼ゲームの設定")
        check_mark = lambda x: '✔︎' if x else ' '
        one_night_kill = '`[{}]`あり\n`[{}]`なし' \
            .format(check_mark(self.one_night_kill), check_mark(not self.one_night_kill))
        one_night_seer = '`[{}]`あり\n`[{}]`なし' \
            .format(check_mark(self.one_night_seer), check_mark(not self.one_night_seer))
        embed.add_field(name='第一夜の襲撃', value=one_night_kill)
        embed.add_field(name='第一夜の占い', value=one_night_seer)
        time = '{}分'.format(self.discuss_time)
        embed.add_field(name='話し合いの時間', value=time, inline=True)
        job_num_text = jobManager.get_job_display_list()
        embed.add_field(name="役職リスト", value=job_num_text)
        players_text = playerManager.get_players_display()
        embed.add_field(name="プレイヤー", value=players_text, inline=True)
        return embed

    def set_one_night_kill(self, onoff:bool):
        self.one_night_kill = onoff
    
    def set_one_night_seer(self, onoff:bool):
        self.one_night_seer = onoff