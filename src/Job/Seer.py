from Job.Job import Job
from Player.Player import Player

class Seer(Job):
    def __init__(self):
        super().__init__(
            job_name='seer',
            job_display_name='占い師'
        )
    
    def action(self, source:Player, target:Player, err=None):
        text = ''
        is_werewolf = lambda x : '人狼' if x=='werewolf' else '市民'
        if not target.get_is_alive():
            text = '死亡者を選択することはできません'
            err = 'error'
            return text, err
        if source == target:
            text = '自分を選択することはできません'
            err = 'error'
            return text, err
        target.reveal_seer()
        text = '{target}を占いました。\n' \
                '{target}は{group}です。' \
                .format(target=target.get_name(),
                        group=is_werewolf(target.get_job().group))
        return text, err
    
    def request_action(self):
        text ='占うプレイヤー(生存者)を**/action**で選択してください。\n' \
                'ex. **/action @player-ほげほげ**'
        return text
    
    def description_action(self):
        text = '目的は生存しているプレイヤーを占い人狼を暴くことです。人狼に襲撃されないように注意してください。'
        return text