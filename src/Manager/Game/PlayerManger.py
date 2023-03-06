import discord
from discord.utils import get
from Player.Player import Player
from Job.Job import Job

class PlayerManager():
    def __init__(self):
        self.player_dict = {
            # key : id -> discord.Guild.id
            # value : player -> Player
        }

    def is_joined_game(self, id:int) -> bool:
        if id in self.player_dict.keys():
            return True
        return False
    # プレイヤーをゲームに登録する
    def register_player(self, name:str, id:int, role:discord.Role,err=None) -> tuple:
        text = name+"さんはもうすでにゲームに参加しています。"
        if self.is_joined_game(id=id):
            print("player ",name," has already joined")
            err = 'error'
            return text, err
        text = name+"さんがゲームに参加しました。"
        player_name = 'player-'+name
        player = Player(name=player_name,id=id,role=role)
        self.player_dict[id] = player
        print("PlayerManager:", self.player_dict)
        return text, err
    
    # プレイヤーをゲームから削除する
    def remove_player(self, name:str, id:int, err=None) -> tuple:
        text = name+"さんはゲームに参加していません。**/join** コマンドで参加することができます"
        if not self.is_joined_game(id=id):
            print("player",name,"don't join the game")
            err = 'error'
            return text, err
        text = name+"さんがゲームから退出しました"
        print("PlayerManager:", self.player_dict)
        self.player_dict.pop(id)
        return text, err

    # プレイヤー数
    def get_player_count(self):
        return len(self.player_dict)
    
    # 生存しているプレイヤー数
    def get_alive_player_count(self):
        count = 0
        for player in self.player_dict.values():
            if player.get_is_alive():
                count += 1
        return count

    # プレイヤーリスト取得
    def get_player_list(self) -> list:
        ret = []
        for p in self.player_dict.values():
            ret.append(p)
        return ret

    # プレイヤーリストをテキスト化
    def get_players_display(self) -> str:
        text = ''
        if not self.player_dict:
            text = ''
        else:
            for user_id in self.player_dict.keys():
                text += f'<@{user_id}> '
        return text
    
    # 生存者(犠牲者)リストをテキスト化
    def get_alive_display(self, is_alive:bool, my_job:Job) -> tuple:
        count = 0
        check_alive = lambda x : '生存者' if x else '犠牲者'
        job_group = lambda x : '市民' if x == 'citizen' else '人狼'
        title = check_alive(is_alive)
        text = ''
        for player in self.player_dict.values():
            if player.get_is_alive() == is_alive:
                text += f'<@&{player.role.id}>'
                if my_job.job_name == 'seer' and player.is_reveal_seer:
                    text += f'({job_group(player.get_job().group)})'
                elif my_job.job_name == 'medium' and player.is_reveal_medium:
                    text += f'({job_group(player.get_job().group)})'
                text += '\n'
                count += 1
        title = f'{title} {count}人'
        return title, text
    def get_player_from_member(self, mem_id:int) -> Player:
        return self.player_dict[mem_id]

    def get_player_from_role(self, name:str) -> Player:
        print(name)
        if not name.startswith('<@&'):
            return None
        role_id = int(name.lstrip('<@&').rstrip('>'))
        for player in self.player_dict.values():
            if role_id == player.role.id:
                return player
        return None
    
    def night_action(self) -> dict:
        max_vote = 0
        kill_players = []
        doubt_players = []
        ret = {}
        for player in self.player_dict.values():
            if player.kill():
                kill_players.append(player)
            if max_vote < player.vote_count:
                max_vote = player.vote_count
                doubt_players.clear()
                doubt_players.append(player)
            elif max_vote == player.vote_count:
                doubt_players.append(player)
        if kill_players:
            ret['kill'] = kill_players
        if doubt_players:
            ret['doubt'] = doubt_players
        return ret
    
    def judgement(self) -> list:
        max_vote = 0
        self.judgement_players = []
        for player in self.player_dict.values():
            if max_vote < player.vote_count:
                max_vote = player.vote_count
                self.judgement_players.clear()
                self.judgement_players.append(player)
            elif max_vote == player.vote_count:
                self.judgement_players.append(player)
        return self.judgement_players

    #決選投票用の表示
    def get_judgement_display(self) -> tuple:
        title = '最多票のプレイヤー'
        text = ''
        for player in self.judgement_players:
            text += f'<@&{player.role.id}>\n'
        return title, text
    
    def reset_players_flags(self):
        for player in self.player_dict.values():
            player.reset_flags()