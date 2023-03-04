from Job.Job import Job
from Player.Player import Player

class Seer(Job):
    def __init__(self):
        super().__init__(
            job_name='seer',
            job_display_name='占い師'
        )
    
    def ability(self, target:Player, err=None):
        text = ''
        check_werewolf = lambda x : '人狼' if x else '市民'
        if not target.get_is_alive():
            text = '死亡者を選択することはできません'
            err = 'error'
        else:
            text = '{target}を占いました。\n' \
                   '{target}は{is_werewolf}です。' \
                   .format(target=target.get_name(),
                           is_werewolf=check_werewolf(target.job.is_werewolf()))
        return text, err
    
    def request_ability(self):
        text ='占うプレイヤー(生存者)を`/ability`で選択してください。\n'
        return text
    
    def description_ability(self):
        text = '役割は生存しているプレイヤーを人狼かどうか占うことです。'
        return text