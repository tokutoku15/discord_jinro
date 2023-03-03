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
        text = 'あなたの役職は{job}です。\n' \
               '占うプレイヤー(死亡者)を選択してください。\n' \
               .format(job=self.job_display_name)
        return text