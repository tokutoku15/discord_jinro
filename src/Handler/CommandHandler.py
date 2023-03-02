from discord import Interaction
from Manager.GameStateManager import GameStateManager

class CommandHandler():
    def __init__(self):
        self.gameStateManager = GameStateManager()

    def join(self, ctx:Interaction, err=None):
        text = '人狼GMbotは休止中です。`/run`コマンドでBotを立ち上げてください。'
        if not self.gameStateManager.get_is_bot_active():
            err = 'error'
            return text,err
        text = 'ゲームが始まっているので参加できません。今のゲームが終わるまでお待ちください。'
        if self.gameStateManager.get_is_game_start():
            err = 'error'
            return text, err
        text = f'{ctx.user.name}が参加しました'
        return text, err

    def exit(self, ctx:Interaction, err=None):
        text = '人狼GMbotは休止中です。`/run`コマンドでBotを立ち上げてください。'
        if not self.gameStateManager.get_is_bot_active():
            err = 'error'
            return text,err
        text = 'ゲームが始まっているので退出できません。今のゲームが終わるまでお待ちください。'
        if self.gameStateManager.get_is_game_start():
            err = 'error'
            return text, err
        text = f'{ctx.user.name}が退出しました'
        return text, err

    def run(self, err=None):
        text = 'もうすでにBotは立ち上がっています。'
        if self.gameStateManager.get_is_bot_active():
            err = 'error'
            return text, err
        text = 'すでにゲームは始まっています。Botが休止している時にこのコマンドを試してください。'
        if self.gameStateManager.get_is_game_start():
            err = 'error'
            return text, err
        self.gameStateManager.active_bot()
        text = '人狼GMbotを起動します。。。おはようございます'
        return text, err

    def start(self, err=None):
        text = '人狼GMbotは休止中です。`/run`コマンドでBotを立ち上げてください。'
        if not self.gameStateManager.get_is_bot_active():
            err = 'error'
            return text, err
        text = 'すでにゲームは始まっています。'
        if self.gameStateManager.get_is_game_start():
            err = 'error'
            return text, err
        self.gameStateManager.game_start()
        text = '今からゲームを始めます。'
        return text, err
    
    def stop(self, err=None):
        text = '人狼GMbotは休止中です。よかったら`/run`コマンドで起こしてください。'
        if not self.gameStateManager.get_is_bot_active():
            err = 'error'
            return text, err
        text = 'ゲーム進行中の場合、ゲームを中断してbotを休止します。おやすみなさいzzz'
        self.gameStateManager.inactive_bot()
        self.gameStateManager.game_stop()
        return text, err

    def ability(self, target, err=None):
        text = '人狼GMbotは休止中です。よかったら`/run`コマンドで起こしてください。'
        if not self.gameStateManager.get_is_bot_active():
            err = 'error'
            return text, err
        text = 'ゲームが始まってないのでこのコマンドは使用できません。'
        if not self.gameStateManager.get_is_game_start():
            err = 'error'
            return text, err
        text = f'{target}を対象に能力を使います。'
        return text, err
    
    def vote(self, target, err=None):
        text = '人狼GMbotは休止中です。よかったら`/run`コマンドで起こしてください。'
        if not self.gameStateManager.get_is_bot_active():
            err = 'error'
            return text, err
        text = 'ゲームが始まってないのでこのコマンドは使用できません。'
        if not self.gameStateManager.get_is_game_start():
            err = 'error'
            return text, err
        text = f'{target}に投票しました。'
        return text, err