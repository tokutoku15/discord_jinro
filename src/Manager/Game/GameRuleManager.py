import discord
from discord import Interaction, ButtonStyle
from Manager.Game.JobManager import JobManager
from Manager.Game.PlayerManger import PlayerManager

class GameRuleManager():
    def __init__(self):
        self.one_night_kill = False
        self.one_night_seer = False
        self.discuss_time = 5
        self.commands = {
            'bot' : {
                '/run' : 'Botの起動・ゲームの設定の開始',
                '/join' : 'ゲームに参加 (Bot起動中)',
                '/exit' : 'ゲームから退出 (Bot起動中)',
                '/start' : 'ゲームの開始',
                '/stop' : 'Botの終了・停止',
            },
            'game' : {
                '/ability' : '役職の能力を使う',
                '/vote' : '処刑するプレイヤーへの投票',
            },
            'game_setting' : {
                '/onenightkill' : '第一夜の襲撃の設定',
                '/onenightseer' : '第一夜の占いの設定',
                '/citizen' : '市民の数の設定',
                '/werewolf' : '人狼の数の設定',
                '/knight' : '騎士の数の設定(max 1)',
                '/seer' : '占い師の数の設定(max 1)',
                'medium' : '霊媒師の数の設定(max 1)',
            }
        }

    def game_setting_Embed(self, jobManager:JobManager, playerManager:PlayerManager) -> discord.Embed:
        embed = discord.Embed(title="人狼ゲームの設定", color=0x20e020)
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
    
    def help_command_Embed(self):
        embed = discord.Embed(title='コマンド一覧')
        bot_commands = '\n'.join([
            '`{}` : {}'.format(cmd, des) for cmd, des in self.commands['bot'].items()
        ])
        embed.add_field(name='Botコマンド', value=bot_commands, inline=True)
        game_commands = '\n'.join([
            '`{}` : {}'.format(cmd, des) for cmd, des in self.commands['game'].items()
        ])
        embed.add_field(name='ゲームコマンド', value=game_commands)
        game_setting_commands = '\n'.join([
            '`{}` : {}'.format(cmd, des) for cmd, des in self.commands['game_setting'].items()
        ])
        embed.add_field(name='ゲーム設定コマンド', value=game_setting_commands)
        return embed

    def set_one_night_kill(self, onoff:bool):
        self.one_night_kill = onoff
    
    def set_one_night_seer(self, onoff:bool):
        self.one_night_seer = onoff