from Player.Player import Player

class PlayerManager():
    def __init__(self):
        self.player_dict = {}

    def is_joined_game(self, id:int) -> bool:
        if id in self.player_dict.keys():
            return True
        return False
    # プレイヤーをゲームに登録する
    def register_player(self, name:str, id:int) -> str:
        text = name+"さんはもうすでにゲームに参加しています。"
        if self.is_joined_game(id=id):
            print("player ",name," has already joined")
            return text
        text = name+"さんがゲームに参加しました。"
        player_name = 'player-'+name
        player = Player(player_name, id)
        self.player_dict[id] = player
        print("PlayerManager:", self.player_dict)
        return text
    
    # プレイヤーをゲームから削除する
    def remove_player(self, name:str, id:int) -> str:
        text = name+"さんはゲームに参加していません。`/join` コマンドで参加することができます"
        if not self.is_joined_game(id=id):
            print("player",name,"don't join the game")
            return text
        text = name+"さんがゲームから退出しました"
        print("PlayerManager:", self.player_dict)
        self.player_dict.pop(id)
        return text

    # プレイヤー数
    def get_player_num(self):
        return len(self.player_dict)
    
    # プレイヤーリストをリセット
    def reset_player_list(self):
        self.player_dict = {}

    # プレイヤーリスト取得
    def get_player_list(self) -> list:
        ret = []
        for p in self.player_dict.values():
            ret.append(p)
        return ret

    # プレイヤーリストをテキスト化
    def get_players_display(self):
        text = ''
        if not self.player_dict:
            text = '参加者0人'
        else:
            plist = '>\n<@!'.join([
                str(user_id)
                for user_id in self.player_dict.keys()
            ])
            text += '<@{}>'.format(plist)
        return text