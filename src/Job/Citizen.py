from Job.Job import Job
from Player.Player import Player

class Citizen(Job):
    def __init__(self):
        super().__init__(
            job_name='citizen',
            job_display_name='市民'
        )
    
    def action(self, source:Player, target:Player, err=None) -> tuple:
        print("Citizen@action")
        if source == target:
            text = '自分を選択することはできません。他の生存者を選択してください。'
            err = 'error'
            return text, err
        if not target.is_alive:
            text = '犠牲者を選択することはできません。生存者を選択してください。'
            err = 'error'
            return text, err
        target.vote()
        text = f'**{target}**を人狼だと疑いました\n'
        return text, err
    
    def request_action(self):
        text = '人狼だと思うプレイヤー(生存者)を **/action** で選択してください。\n' \
                'ex. **/action @player-ほげほげ**'
        return text
    
    def description_action(self):
        text = '目的は全ての人狼を処刑して市民陣営が勝つことです。'
        return text