from Job.Job import Job
from Player.Player import Player

class Seer(Job):
    def __init__(self):
        super().__init__(
            job_name='seer',
            job_display_name='占い師'
        )
    
    def action(self, source:Player, target:Player, err=None) -> tuple:
        is_werewolf = lambda x : '人狼:werewolf:' if x=='werewolf' else '市民:citizen:'
        target.seer()
        if source == target:
            text = '自分を選択することはできません。他の生存者を選択してください。'
            err = 'error'
            return text, err
        if not target.is_alive:
            text = '犠牲者を選択することはできません。生存者を選択してください。'
            err = 'error'
            return text, err
        if target.is_reveal:
            text = f'もう{target}は占っています。占っていないプレイヤーを選択してください。'
            err = 'error'
            return text, err
        text = f'**{target}**を占いました。\n' \
                f'{target} は **{is_werewolf(target.job.appear_group)}** です'
        return text, err
    
    def request_action(self):
        text ='占うプレイヤー(生存者)を**/action**で選択してください。\n' \
                'ex. **/action @player-ほげほげ**'
        return text
    
    def description_action(self):
        text = '目的は生存しているプレイヤーを占い人狼を暴くことです。人狼に襲撃されないように注意してください。'
        return text