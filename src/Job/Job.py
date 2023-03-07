from abc import ABCMeta, abstractmethod
from discord import Emoji

class Job(metaclass=ABCMeta):
    def __init__(self, 
                job_name:str, 
                job_display_name:str,
                appear_group:str='citizen',
                group:str='citizen'
        ):
        self.job_name = job_name
        self.job_display_name = job_display_name
        # 占い師や霊媒師からどちらの陣営に見えるか
        # 見かけの陣営
        self.appear_group = appear_group
        # 実際の陣営
        self.group = group
        self.emoji:Emoji = None
    def __str__(self):
        return f'{self.emoji}{self.job_display_name}'
    def set_emoji(self, emoji:Emoji):
        self.emoji = emoji
    def get_emoji(self):
        return self.emoji

    @abstractmethod
    def action(self):
        raise NotImplementedError
    @abstractmethod
    def request_action(self):
        raise NotImplementedError
    @abstractmethod
    def description_action(self):
        raise NotImplementedError