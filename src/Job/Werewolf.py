from Job.Job import Job
from Player.Player import Player

class Werewolf(Job):
    def __init__(self):
        super().__init__(
            job_name='werewolf',
            job_display_name='人狼',
            is_werewolf=True
        )
    
    def ability(self, target:Player, err=None):
        text = ''
        if not target.get_is_alive():
            text = '死亡者を選択することはできません'
            err = 'error'
        else:
            text = '{target}を襲撃対象にしました。\n' \
                   .format(target=target.get_name())
        return text, err
    
    def request_ability(self):
        text = '襲撃するプレイヤー(生存者)を`/ability`で選択してください。\n'
        return text
    
    def description_ability(self):
        text = '役割は市民を襲撃して人狼陣営が勝つことです。市民に正体を見破られてはいけません。'
        return text