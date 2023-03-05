import random
from Job.Citizen import Citizen
from Job.Werewolf import Werewolf
from Job.Seer import Seer
from Job.Medium import Medium
from Job.Knight import Knight

class JobManager():
    def __init__(self):
        self.job_num_dict = {
            'citizen' : [Citizen(), 0],
            'werewolf' : [Werewolf(), 0],
            'knight' : [Knight(), 0],
            'seer' : [Seer(), 0],
            'medium' : [Medium(), 0],
        }
        self.max_limited_job = [
            'knight', 'seer', 'medium'
        ]
    
    def register_job_emoji(self, emoji_list:list):
        for emoji in emoji_list:
            if not emoji.name in self.job_num_dict.keys():
                continue
            self.job_num_dict[emoji.name][0].set_emoji(emoji)
    
    def get_display_list(self) -> str:
        text = ''
        for k, v in self.job_num_dict.items():
            print(str(v[0]), v[1])
            text += '{} : `{}`人'.format(v[0],v[1])
            if k in self.max_limited_job:
                text += '(max 1)'
            text += '\n'
        return text
    
    def set_job_num(self, job_name:str, num:int):
        if num < 0:
            return
        if job_name in self.max_limited_job:
            num = min(1, num)
        self.job_num_dict[job_name][1] = num
    
    def set_default_num(self, member_num:int):
        self.job_num_dict['citizen'][1] = member_num - 1
        self.job_num_dict['werewolf'][1] = 1
    
    def get_stack(self):
        job_stack = []
        for v in self.job_num_dict.values():
            for _ in range(v[1]):
                job_stack.append(v[0])
        random.shuffle(job_stack)
        return job_stack
    
    # 市民陣営の人数(市民:人狼)
    def get_group_count(self) -> tuple:
        citizen_count = 0
        werewolf_count = 0
        for v in self.job_num_dict.values():
            if type(v[0]) == Werewolf:
                werewolf_count += v[1]
            else:
                citizen_count += v[1]
        return citizen_count, werewolf_count