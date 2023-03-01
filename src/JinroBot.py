# coding:utf-8
import discord
from discord import app_commands
from discord_buttons_plugin import *
from discord.utils import get
'''
自作ライブラリ
'''
from Manager.RoleManager import RoleManager
from Manager.TextChannelManager import TextChannelManager

class JinroBot(discord.Client):
    def __init__(self,gid:int,tcid:int,vcid:int):
        super().__init__(
            intents = discord.Intents.all()
        )
        self.buttons = ButtonsClient(super())
        self.tree = app_commands.CommandTree(super())
        self.game_guild = self.get_guild(gid)
        self.game_text_channel = self.get_channel(tcid)
        self.game_voice_channel = self.get_channel(vcid)