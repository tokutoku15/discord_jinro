from abc import ABCMeta, abstractmethod
from discord import Emoji

class Job(metaclass=ABCMeta):
    def __init__(self, job_name:str, job_display_name:str, is_werewolf:bool=False):
        self.job_name = job_name
        self.job_display_name = job_display_name
        self.is_werewolf = is_werewolf
        self.emoji = None
    
    def __str__(self):
        return f'{self.job_display_name}'
    def set_is_werewolf(self, is_werewolf:bool):
        self.is_werewolf = is_werewolf
    
    def get_display_name(self) -> str:
        return f'{self.job_display_name}{self.emoji}'
    def is_werewolf(self) -> bool:
        return self.is_werewolf

    def set_emoji(self, emoji:Emoji):
        self.emoji = emoji
    def get_emoji(self):
        return self.emoji

    @abstractmethod
    def ability(self):
        raise NotImplementedError
    @abstractmethod
    def request_ability(self):
        raise NotImplementedError
    @abstractmethod
    def description_ability(self):
        raise NotImplementedError