from Job.Job import Job

class Player():
    def __init__(self, name:str, id:int):
        self.name = name
        self.id = id
        self.is_alive = True
        self.job = None
    def get_name(self) -> str:
        return self.name
    def get_is_alive(self) -> bool:
        return self.is_alive
    def reset(self):
        self.is_alive = True
    def add_job(self, job:Job):
        self.job = job