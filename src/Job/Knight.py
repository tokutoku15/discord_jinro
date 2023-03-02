from Job.Job import Job
from Player.Player import Player

class Knight(Job):
    def __init__(self):
        super().__init__(
            job_name='knight',
            job_display_name='騎士'
        )
    
    def ability(self, target:Player, err=None):
        text = ''
        if not target.get_is_alive():
            text = '死亡者を選択することはできません'
            err = 'error'
        else:
            text = '{target}を人狼から守ります\n' \
                   .format(target=target.get_name())
        return text, err
    
    def request_ability(self):
        text = 'あなたの役職は{job}です。\n' \
               '人狼から守るプレイヤー(生存者)を選択してください。\n' \
               .format(job=self.job_display_name)
        return text