from Job.Job import Job
from Player.Player import Player

class Werewolf(Job):
    def __init__(self):
        super().__init__(
            job_name='werewolf',
            job_display_name='人狼',
            group='werewolf'
        )
    
    def action(self, source:Player, target:Player, err=None):
        text = ''
        if not target.get_is_alive():
            text = '死亡者を選択することはできません'
            err = 'error'
            return text, err
        if target.get_job().group == self.group:
            text = '仲間の人狼を選択することはできません'
            err = 'error'
            return text, err
        if source == target:
            text = '自分を選択することはできません'
            err = 'error'
            return text, err
        text = '{target}を襲撃対象にしました。\n' \
                   .format(target=target.get_name())
        target.kill()
        return text, err
    
    def request_action(self):
        text = '襲撃するプレイヤー(生存者)を**/action**で選択してください。\n' \
                'ex. **/action @player-ほげほげ**'
        return text
    
    def description_action(self):
        text = '目的は市民を襲撃して人狼陣営が勝つことです。市民に正体を見破られてはいけません。'
        return text