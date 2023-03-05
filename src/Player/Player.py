import discord
from Job.Job import Job

class Player():
    def __init__(self, name:str, id:int):
        self.name = name
        self.id = id
        self.job = None
        self.my_channel = None

    def get_name(self) -> str:
        return self.name
    def get_is_alive(self) -> bool:
        return self.is_alive
    def reset(self):
        self.is_alive = True
    def add_job(self, job:Job):
        self.job = job
    def get_job(self):
        return self.job
    def set_channel(self, channel:discord.TextChannel):
        self.my_channel = channel
    def get_channel(self) -> discord.TextChannel:
        return self.my_channel