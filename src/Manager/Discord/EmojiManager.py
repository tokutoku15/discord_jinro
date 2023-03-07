from discord import Guild

class EmojiManager():
    def __init__(self, guild:Guild):
        self.guild = guild
        self.emoji_list = {}
        self.emoji_name_list = [
            'citizen',
            'werewolf',
            'knight',
            'seer',
            'medium',
            'madman',
        ]
        self.register_emojis()
    
    def register_emojis(self):
        for emoji in self.guild.emojis:
            if emoji.name in self.emoji_name_list:
                self.emoji_list[emoji.name] = emoji
                print(emoji)
    
    def get_emoji_list(self) -> dict:
        return self.emoji_list