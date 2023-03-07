from Job.Job import Job
from Player.Player import Player

class Knight(Job):
    def __init__(self):
        super().__init__(
            job_name='knight',
            job_display_name='騎士'
        )
    
    def action(self, source:Player,target:Player, err=None) -> tuple:
        if source == target:
            text = '自分を選択することはできません。他の生存者を選択してください。'
            err = 'error'
            return text, err
        if not target.is_alive:
            text = '犠牲者を選択することはできません。生存者を選択してください。'
            err = 'error'
            return text, err
        target.protect()
        text = f'**{target}**を人狼から守ります\n'
        return text, err
    
    def request_action(self):
        text = '人狼から守るプレイヤー(生存者)を**/action**で選択してください。\n' \
                'ex. **/action @player-ほげほげ**'
        return text

    def description_action(self):
        text = '目的は人狼の襲撃からプレイヤーを守ることです。'
        return text