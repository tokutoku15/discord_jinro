from discord import Role, TextChannel
from Job.Job import Job

class Player():
    def __init__(self, name:str, id:int, role:Role):
        # プレイヤー情報
        self.name = name
        self.id = id
        self.role = role
        self.channel:TextChannel = None
        # ゲーム内に関する情報
        self.has_acted = False
        self.vote_count = 0
        self.is_alive = True
        self.is_reveal = False
        self.is_protected = False
        self.will_be_kill = False
        self.job:Job = None
    def __str__(self):
        return self.name
    # 自分のチャンネルを割り当てる
    def set_channel(self, channel:TextChannel):
        self.channel = channel
    # ゲームの役職を割り当てる
    def assign_job(self, job:Job):
        self.job = job
    # 自分に投票される
    def vote(self):
        self.vote_count += 1
    # 占い師に占われる
    def seer(self):
        self.is_reveal = True
    # 騎士に防衛されるフラグを立てる
    def protect(self):
        self.is_protected = True
    # 人狼に襲撃されるフラグを立てる
    def will_kill(self):
        self.will_be_kill = True
    # フラグをリセットする
    def reset_flags(self):
        self.vote_count = 0
        self.has_acted = False
        self.is_protected = False
        self.will_be_kill = False
    # 犠牲者となる
    def fall_victim(self):
        self.is_alive = False
    # アクション(アクション、投票)が終了
    def finish_act(self):
        self.has_acted = True
    # アクションのリセット
    def reset_act(self):
        self.has_acted = False
    # ゲーム終了後のリセット
    def reset_all_flags(self):
        self.is_alive = True
        self.has_acted = False
        self.vote_count = 0
        self.is_reveal = False
        self.is_protected = False
        self.will_be_kill = False
        self.job:Job = None