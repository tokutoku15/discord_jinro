import random
from Job.Citizen import Citizen
from Job.Werewolf import Werewolf
from Job.Seer import Seer
from Job.Medium import Medium
from Job.Knight import Knight

class JobManager():
    def __init__(self):
        self.job_num_dict = {
            1 : [Citizen(), 0],
            2 : [Werewolf(), 0],
            3 : [Knight(), 0],
            4 : [Seer(), 0],
            5 : [Medium(), 0],
        }
    
    def get_job_display_list(self) -> str:
        text = ''
        for k, v in self.job_num_dict.items():
            print(k, str(v[0]), v[1])
            text += '[{}]{} : `{}`人\n'.format(k,str(v[0]),v[1])
        return text
    
    def set_job_num(self, id:int, num:int):
        self.job_num_dict[id][1] = num
    
    def set_default_num(self, member_num:int):
        self.job_num_dict[1][1] = member_num - 1
        self.job_num_dict[2][1] = 1
    
    def get_job_stack(self):
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