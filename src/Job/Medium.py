from Job.Job import Job
from Player.Player import Player

class Medium(Job):
    def __init__(self):
        super().__init__(
            job_name='medium',
            job_display_name='霊媒師'
        )
    
    def action(self, target:Player, err=None):
        text = ''
        is_werewolf = lambda x : '人狼' if x=='werewolf' else '市民'
        if target.get_is_alive():
            text = '生存者を選択することはできません'
            err = 'error'
        else:
            target.reveal_medium()
            text = '{target}を占いました。\n' \
                   '{target}は{group}です。' \
                   .format(target=target.get_name(),
                           group=is_werewolf(target.job.group))
        return text, err
    
    def request_action(self):
        text = '占うプレイヤー(死亡者)を`/action`で選択してください。\n'
        return text
    
    def description_action(self):
        text = '目的は死亡したプレイヤーを占い、人狼を暴くことです。'
        return text