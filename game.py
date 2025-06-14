import random
import string
from typing import List, Optional, Dict
from player import Player
from game_record import GameRecord

class Game:
    def __init__(self, player_configs: List[Dict[str, str]]) -> None:
        """初始化游戏

        Args:
            player_configs: 包含玩家配置的列表，每个配置是一个字典，包含 name 和 model 字段
        """
        self.players = [Player(config["name"], config["model"]) for config in player_configs]

        for player in self.players:
            player.init_opinions(self.players)

        # 洗牌名称映射：匿名名 -> 原始名
        self.name_mapping = self.shuffle_player_names(self.players)

        self.game_over: bool = False

        self.game_record: GameRecord = GameRecord()
        self.game_record.start_game([p.name for p in self.players])
        self.round_count = 0

    def shuffle_player_names(self, players: List[Player]) -> Dict[str, str]:
        """
        洗牌：为每个玩家分配一个匿名名字，并建立映射
        返回匿名名 -> 原始名 的映射字典
        """
        used_names = set()
        name_mapping = {}

        for player in players:
            while True:
                random_id = ''.join(random.choices(string.digits, k=3))
                anon_name = f"player-{random_id}"
                if anon_name not in used_names:
                    break
            used_names.add(anon_name)
            name_mapping[anon_name] = player.name
            player.game_name = anon_name  # 绑定匿名名供模型调用

        return name_mapping

    def deshuffle_name(self, anon_name: str) -> str:
        """
        还原：从匿名名映射回原始名
        """
        return self.name_mapping.get(anon_name, anon_name)

    def check_victory(self) -> bool:
        """
        检查胜利条件（仅剩两名存活玩家时），并记录胜利者
        """
        alive_players = [p for p in self.players if p.alive]
        if len(alive_players) == 2:
            winner_names = [p.name for p in alive_players]
            print(f"\n游戏结束，幸存者：{winner_names}")
            self.game_record.finish_game(winner_names)
            self.game_over = True
            return True
        return False

    def handle_reflection(self) -> None:
        """
        处理所有存活玩家的反思过程
        """
        alive_players = [p for p in self.players if p.alive]
        alive_player_names = [p.name for p in alive_players]
        round_base_info = self.game_record.get_latest_round_info()

        for player in alive_players:
            round_action_info = self.game_record.get_latest_round_actions(player.name, include_latest=True)
            round_result = self.game_record.get_latest_round_result(player.name)

            player.reflect(
                alive_players=alive_player_names,
                round_base_info=round_base_info,
                round_action_info=round_action_info,
                round_result=round_result
            )

        return alive_players

    def start_game(self) -> None:
        """游戏主循环（待重构为清剿模式）"""
        print("游戏开始！")
        print("玩家名称洗牌映射如下：")
        for anon, real in self.name_mapping.items():
            print(f"  {anon} -> {real}")
        print("-" * 50)

        while not self.game_over:
            print("TODO: 实现清剿博弈轮次逻辑")
            break

if __name__ == '__main__':
    player_configs = [
        {"name": "DeepSeek", "model": "deepseek-ai/DeepSeek-R1"},
        {"name": "QwQ", "model": "Qwen/QwQ-32B"},
        {"name": "Qwen3", "model": "Qwen/Qwen3-235B-A22B"},
        {"name": "Gemini", "model": "gemini-2.0-flash-thinking-exp"}
    ]

    print("游戏开始！玩家配置如下：")
    for config in player_configs:
        print(f"玩家：{config['name']}, 使用模型：{config['model']}")
    print("-" * 50)

    game = Game(player_configs)
    game.start_game()
