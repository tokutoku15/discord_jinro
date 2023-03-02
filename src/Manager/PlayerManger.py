import discord
from discord import Member
from discord.utils import get
from Player.Player import Player

class PlayerManager():
    def __init__(self):
        self.player_dict = {}
    def is_joined_game(self, member:Member) -> bool:
        if member.id in self.player_dict.keys():
            return True
        return False
    # プレイヤーをゲームに登録する
    def register_player(self, member:Member) -> str:
        text = member.name+"さんはもうすでにゲームに参加しています。"
        if self.is_joined_game(member=member):
            print("player ",member.name," has already joined")
            return text
        text = member.name+"さんがゲームに参加しました。"
        print("PlayerManager:", self.player_dict)
        player_name = 'player-'+member.name
        player = Player(player_name, member.id)
        self.player_dict[member.id] = player
        return text
    
    # プレイヤーをゲームから削除する
    def remove_player(self, member:Member) -> str:
        text = member.name+"さんはゲームに参加していません。`/join` コマンドで参加することができます"
        if not self.is_joined_game(member=member):
            print("player",member.name,"don't join the game")
            return text
        text = member.name+"さんがゲームから退出しました"
        print("PlayerManager:", self.player_dict)
        self.player_dict.pop(member.id)
        return text

    # プレイヤーリスト取得
    def get_player_list(self) -> list:
        ret = []
        for p in self.player_dict.values():
            ret.append(p)
        return ret