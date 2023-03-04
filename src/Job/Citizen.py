from Job.Job import Job
from Player.Player import Player

class Citizen(Job):
    def __init__(self):
        super().__init__(
            job_name='citizen',
            job_display_name='市民'
        )
    
    def ability(self, target:Player, err=None):
        text = ''
        if not target.get_is_alive():
            text = '死亡者を選択することはできません'
            err = 'error'
        else:
            text = '人狼だと思うプレイヤーは{target}です\n' \
                   .format(target=target.get_name())
        return text, err
    
    def request_ability(self):
        text = '人狼だと思うプレイヤーを`/ability`で選択してください。\n'
        return text
    
    def description_ability(self):
        text = '役割は人狼を処刑して市民陣営が勝つことです。'
        return text