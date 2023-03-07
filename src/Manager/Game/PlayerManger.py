import discord
from discord.utils import get
from Player.Player import Player
from Job.Job import Job

class PlayerManager():
    def __init__(self):
        self.player_dict = {
            # key : member -> discord.Member
            # value : player -> Player
        }
    def reset_players(self):
        self.__init__()
    # プレイヤーがゲームに参加しているか
    def is_joined_game(self, member:discord.Member) -> bool:
        if member in self.player_dict.keys():
            return True
        return False
    # プレイヤーをゲームに登録する
    def register_player(self, member:discord.Member, role:discord.Role,err=None) -> tuple:
        text = member.name+"さんはもうすでにゲームに参加しています。"
        if self.is_joined_game(member=member):
            print("player ",member.name," has already joined")
            err = 'error'
            return text, err
        text = member.name+"さんがゲームに参加しました。"
        player_name = 'player-'+member.name
        player = Player(name=player_name,id=member.id,role=role)
        self.player_dict[member] = player
        print("PlayerManager:", self.player_dict)
        return text, err
    # プレイヤーをゲームから削除する
    def remove_player(self, member:discord.Member, err=None) -> tuple:
        text = member.name+"さんはゲームに参加していません。**/join** コマンドで参加することができます"
        if not self.is_joined_game(member=member):
            print("player",member.name,"don't join the game")
            err = 'error'
            return text, err
        text = member.name+"さんがゲームから退出しました"
        print("PlayerManager:", self.player_dict)
        self.player_dict.pop(member)
        return text, err
    # プレイヤー数
    def get_player_count(self):
        return len(self.player_dict)
    # 生存しているプレイヤー数
    def get_alive_player_count(self):
        count = 0
        for player in self.player_dict.values():
            if player.is_alive:
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
            for user in self.player_dict.keys():
                text += f'<@{user.id}>'
        return text
    # プレイヤーにジョブを割り当てる
    def assign_jobs(self, job_stack:list):
        for player in self.player_dict.values():
            player.assign_job(job_stack.pop(0))
    # 生存者(犠牲者)リストをテキスト化
    def get_alive_display(self, is_alive:bool, my_job:Job) -> tuple:
        count = 0
        check_alive = lambda x : '生存者' if x else '犠牲者'
        job_group = lambda x : '市民' if x == 'citizen' else '人狼'
        title = check_alive(is_alive)
        text = ''
        for player in self.player_dict.values():
            if player.is_alive == is_alive:
                text += f'<@&{player.role.id}>'
                if my_job.job_name == 'medium' and not player.is_alive:
                    text += f'({job_group(player.job.appear_group)})'
                elif my_job.job_name == 'seer' and player.is_reveal:
                    text += f'({job_group(player.job.appear_group)})'
                text += '\n'
                count += 1
        title += f' {count}人'
        return title, text
    # 投票用(他のプレイヤーの投票状況が見られるように)
    def get_vote_count_display(self) -> tuple:
        title = '投票できるプレイヤー'
        text = ''
        for player in self.player_dict.values():
            if player.is_alive:
                text += f'<@&{player.role.id}> ({player.vote_count}票)\n'
        return title, text
    # 犠牲者が今の状況をみられるように
    def get_player_state_display(self, is_alive:bool) -> tuple:
        count = 0
        check_alive = lambda x : '生存者' if x else '犠牲者'
        title = check_alive(is_alive)
        text = ''
        for player in self.player_dict.values():
            if player.is_alive == is_alive:
                text += f'<@&{player.role.id}>({player.job})\n'
                count += 1
        title += f' ({count}人)'
        return title, text
    def get_player_from_member(self, mem:discord.Member) -> Player:
        return self.player_dict[mem]
    # ロール(id)からプレイヤーを取得
    def get_player_from_role(self, name:str) -> Player:
        if not name.startswith('<@&'):
            return None
        role_id = int(name.lstrip('<@&').rstrip('>'))
        for player in self.player_dict.values():
            if role_id == player.role.id:
                return player
        return None
    
    def night_action_result(self) -> dict:
        max_vote = 0
        kill_players = []
        doubt_players = []
        ret = {}
        for player in self.player_dict.values():
            if player.will_kill():
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
            if player.is_alive:
                player.reset_flags()
            player.reset_vote_count()