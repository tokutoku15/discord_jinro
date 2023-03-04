import discord

class EmojiManager():
    def __init__(self):
        self.guild = None
        self.emoji_list = {}
        self.emoji_name_list = [
            'citizen',
            'werewolf',
            'knight',
            'seer',
            'medium',
            'madman',
        ]

    def register_guild(self, guild:discord.Guild):
        self.guild = guild    
    
    def register_emojis(self):
        for emoji in self.guild.emojis:
            if emoji.name in self.emoji_name_list:
                self.emoji_list[emoji.name] = emoji
                print(emoji)