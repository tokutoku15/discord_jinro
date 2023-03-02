class GameStateManager():
    def __init__(self):
        self.is_bot_active = False
        self.is_game_start = False
        self.game_phase = {
            10 : 'result',
            20 : 'setting',
            0  : 'night',
            1  : 'morning',
            2  : 'discuss',
            3  : 'vote',
        }
        self.now_phase = 20
    
    def game_end(self):
        self.now_phase = 10
    def game_setting(self):
        self.now_phase = 20
    def next_phase(self):
        self.now_phase += 1
        self.now_phase %= 4
    def get_now_state(self) -> str:
        return self.game_phase[self.now_phase]

    def active_bot(self):
        self.is_bot_active = True
        self.game_setting()
    def inactive_bot(self):
        self.is_bot_active = False
    def game_start(self):
        self.is_game_start = True
        self.game_setting()
    def game_stop(self):
        self.is_game_start = False
    
    def get_is_bot_active(self) -> bool:
        return self.is_bot_active
    def get_is_game_start(self) -> bool:
        return self.is_game_start