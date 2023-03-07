class GameStateManager():
    def __init__(self):
        self.game_phase = {
            10 : 'wait',
            20 : 'setting',
            0  : 'night',
            1  : 'morning',
            2  : 'discuss',
            3  : 'vote',
            4  : 'result',
        }
        self.day = 1
        self.now = 10

    def game_wait(self):
        self.now = 10
        self.day = 1
    def game_setting(self):
        self.now = 20
    def game_start(self):
        self.now = 0
    def next_phase(self):
        self.now += 1
        self.now %= 4
    def game_result(self):
        self.now = 4
    def next_day(self):
        self.day += 1
    def reset_day(self):
        self.day = 1
    def get_now_phase(self):
        return self.game_phase[self.now]