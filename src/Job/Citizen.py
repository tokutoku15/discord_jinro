from Job.Job import Job
from Player.Player import Player

class Citizen(Job):
    def __init__(self):
        super().__init__(
            job_name='citizen',
            job_display_name='市民'
        )
    
    def action(self, source:Player, target:Player, err=None):
        text = ''
        if source == target:
            text = '自分を選択することはできません'
            err = 'error'
            return text, err
        if not target.get_is_alive():
            text = '死亡者を選択することはできません'
            err = 'error'
            return text, err
        text = '人狼だと思うプレイヤーは{target}です\n' \
                   .format(target=target.get_name())
        target.vote()
        return text, err
    
    def request_action(self):
        text = '人狼だと思うプレイヤー(生存者)を**/action**で選択してください。\n' \
                'ex. **/action @player-ほげほげ**'
        return text
    
    def description_action(self):
        text = '目的は人狼を処刑して市民陣営が勝つことです。'
        return text