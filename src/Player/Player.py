import discord
from Job.Job import Job

class Player():
    def __init__(self, name:str, id:int, role:discord.Role):
        self.name = name
        self.id = id
        self.role = role
        self.job = None
        self.my_channel = None
        self.is_alive = True
        self.is_reveal_seer = False
        self.is_reveal_medium = False
        self.is_protected = False
        self.will_be_killed = False
        self.vote_count = 0

    def __str__(self):
        return self.name
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
    def reveal_seer(self):
        self.is_reveal_seer = True
    def get_reveal_seer(self):
        return self.is_reveal_seer
    def reveal_medium(self):
        self.is_reveal_medium = True
    def get_reveal_medium(self):
        return self.is_reveal_medium
    def vote(self):
        self.vote_count += 1
    def reset_vote(self):
        self.vote_count = 0
    def protect(self):
        self.is_protected = True
    def get_protect(self):
        return self.is_protected
    def kill(self):
        self.will_be_killed = True
    def get_kill(self):
        self.will_be_killed = True
    def reset_flags(self):
        self.is_protected = False
        self.will_be_killed = False
        self.vote_count = 0