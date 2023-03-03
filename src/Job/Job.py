from abc import ABCMeta, abstractmethod

class Job(metaclass=ABCMeta):
    def __init__(self, job_name:str, job_display_name:str, is_werewolf:bool=False):
        self.job_name = job_name
        self.job_display_name = job_display_name
        self.is_werewolf = is_werewolf
    
    def __str__(self):
        return self.job_display_name
    
    def set_job_name(self, name:str):
        self.job_name = name
    def set_job_display_name(self, name:str):
        self.job_display_name = name
    def set_is_werewolf(self, is_werewolf:bool):
        self.is_werewolf = is_werewolf
    
    def get_job_display_name(self) -> str:
        return self.job_display_name
    def is_werewolf(self) -> bool:
        return self.is_werewolf

    @abstractmethod
    def ability(self):
        raise NotImplementedError
    @abstractmethod
    def request_ability(self):
        raise NotImplementedError