import discord
import random
from Manager.Game.PlayerManger import PlayerManager
from Job.Citizen import Citizen
from Job.Werewolf import Werewolf
from Job.Knight import Knight
from Job.Seer import Seer
from Job.Medium import Medium
from Job.Madman import Madman

class GameRuleManager():
    def __init__(self):
        self.one_night_kill = False
        self.one_night_seer = False
        self.setting_discuss_time = 300
        self.discuss_time = self.setting_discuss_time
        self.job_num = {
            Citizen() : 0,
            Werewolf() : 0,
            Knight() : 0,
            Seer() : 0,
            Medium() : 0,
            Madman() : 0,
        }
        self.setting_color = 0x40d040
        self.commands = {
            'bot' : {
                '/game' : 'ゲームの設定の開始',
                '/join' : 'ゲームに参加',
                '/exit' : 'ゲームから退出',
                '/start' : 'ゲームの開始',
                '/stop' : 'ゲーム・Botの終了',
            },
            'game' : {
                '/action' : '役職の能力を使う',
                '/vote' : 'プレイヤーへの投票',
            },
            'game_setting' : {
                '/menu' : '第一夜の行動の設定',
                '/job'  : '役職の人数の設定',
            },
            'color' : 0x348cac,
        }
    # ゲームルールの初期化
    def reset_rule(self):
        self.one_night_kill = False
        self.one_night_seer = False
        self.setting_discuss_time = 300
        self.discuss_time = self.setting_discuss_time
        for k in self.job_num.keys():
            self.job_num[k] = 0
    # 第一夜の襲撃の設定を変更
    def set_one_night_kill(self, onoff:bool):
        self.one_night_kill = onoff
    # 第一夜の占いの設定を変更
    def set_one_night_seer(self, onoff:bool):
        self.one_night_seer = onoff
    # ジョブの人数を設定
    def set_job_num(self, name:str, num:int):
        if num < 0 : return
        for job in self.job_num.keys():
            if name == job.job_name:
                self.job_num[job] = num
    # 時間のセット
    def set_time(self, time:int):
        self.discuss_time = time
    # 残り時間を加える
    def add_time(self, time:int):
        self.discuss_time += time
    # 残り時間のリセット
    def reset_time(self):
        self.discuss_time = self.setting_discuss_time
    # ジョブグループの人数取得
    def get_group_num(self) -> tuple:
        citizen = 0
        werewolf = 0
        for job, num in self.job_num.items():
            if job.appear_group == 'citizen':
                citizen += num
            else:
                werewolf += num
        return citizen, werewolf
    # 設定したジョブ人数の合計
    def get_job_sum(self):
        sum = 0
        for n in self.job_num.values():
            sum += n
        return sum
    # ランダムに入れ替えたジョブ割り当て用のリスト
    def get_job_stack(self):
        ret = []
        for job, num in self.job_num.items():
            for _ in range(num):
                ret.append(job)
        random.shuffle(ret)
        return ret
    # ジョブにDiscord絵文字をセット
    def set_job_emoji(self, emojis:dict):
        for job in self.job_num.keys():
            job.set_emoji(emojis[job.job_name])
    # ジョブの絵文字urlを取得
    def get_job_url(self, name:str) -> str:
        url = 'https://cdn.discordapp.com/emojis/'
        for job in self.job_num.keys():
            if job.job_name == name:
                url += str(job.get_emoji().id)
        return url
    # gameコマンドで呼び出されるゲーム設定の埋め込みテキスト
    def game_setting_embed(self, pManager:PlayerManager) -> discord.Embed:
        embed = discord.Embed(title='#### 人狼ゲームの設定 ####', color=self.setting_color)
        check = lambda x: '✔︎' if x else ' '
        one_night_kill = '`[{}]`あり\n`[{}]`なし' \
            .format(check(self.one_night_kill), check(not self.one_night_kill))
        one_night_seer = '`[{}]`あり\n`[{}]`なし' \
            .format(check(self.one_night_seer), check(not self.one_night_seer))
        embed.add_field(name='第一夜の襲撃', value=one_night_kill, inline=True)
        embed.add_field(name='第一夜の占い', value=one_night_seer, inline=True)
        time = '{:02d}分{:02d}秒'.format(self.discuss_time//60, self.discuss_time%60)
        embed.add_field(name='話し合いの時間', value=time, inline=True)
        job_num_text = '\n'.join([
            '{}{} : **{}**人'.format(job.get_emoji(),job,num)
            for job, num in self.job_num.items()
        ])
        job_sum = self.get_job_sum()
        embed.add_field(name=f'役職一覧 ({job_sum}人)', value=job_num_text)
        players_text = pManager.get_players_display()
        players_num = pManager.get_player_count()
        embed.add_field(name=f'参加者 ({players_num}人)', value=players_text)
        return embed
    # helpコマンドで呼び出される埋め込みテキスト
    def bot_command_embed(self) -> discord.Embed:
        embed = discord.Embed(title='#### コマンド一覧 ####', color=self.commands['color'])
        bot_commands = '\n'.join([
            '> {} : {}'.format(cmd, des) for cmd, des in self.commands['bot'].items()
        ])
        embed.add_field(name='Botコマンド', value=bot_commands, inline=True)
        game_setting_commands = '\n'.join([
            '> {} : {}'.format(cmd, des) for cmd, des in self.commands['game_setting'].items()
        ])
        embed.add_field(name='ゲーム設定コマンド', value=game_setting_commands, inline=True)
        game_commands = '\n'.join([
            '> {} : {}'.format(cmd, des) for cmd, des in self.commands['game'].items()
        ])
        embed.add_field(name='ゲームコマンド', value=game_commands, inline=False)
        return embed