from Job.Job import Job
from Player.Player import Player

class Medium(Job):
    def __init__(self):
        super().__init__(
            job_name='Medium',
            job_display_name='霊媒師'
        )
    
    def ability(self, target:Player, err=None):
        text = ''
        if target.get_is_alive():
            text = '生存者を選択することはできません'
            err = 'error'
        else:
            text = '{target}を人狼から守ります\n' \
                   .format(target=target.get_name())
        return text, err
    
    def request_ability(self):
        text = '占うプレイヤー(死亡者)を`/ability`で選択してください。\n'
        return text
    
    def description_ability(self):
        text = '役割は死亡したプレイヤーが人狼かどうかを占うことです。'