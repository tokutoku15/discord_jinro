from Job.Job import Job
from Player.Player import Player

class Knight(Job):
    def __init__(self):
        super().__init__(
            job_name='knight',
            job_display_name='騎士'
        )
    
    def action(self, source:Player,target:Player, err=None):
        text = ''
        if not target.get_is_alive():
            text = '死亡者を選択することはできません'
            err = 'error'
            return text, err
        if source == target:
            text = '自分を選択することはできません'
            err = 'error'
            return text, err
        target.protect()
        text = '{target}を人狼から守ります\n' \
                   .format(target=target.get_name())
        return text, err
    
    def request_action(self):
        text = '人狼から守るプレイヤー(生存者)を**/action**で選択してください。\n' \
                'ex. **/action @player-ほげほげ**'
        return text

    def description_action(self):
        text = '目的は人狼の襲撃からプレイヤーを守ることです。'
        return text