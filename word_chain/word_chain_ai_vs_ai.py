import time
import sys
from ai_player import get_ai_idiom, initialize_client_manually, validate_idiom_chain

MAX_ROUNDS = 100
PLAYER_MODELS = {
    1: "gpt-4o",
    2: "gpt-4o-mini"
}

class AIIdiomChainGame:
    def __init__(self, max_rounds=MAX_ROUNDS):
        self.game_history = []
        self.current_idiom = ""
        self.round_count = 0
        self.max_rounds = max_rounds
        self.scores = {1: 0, 2: 0}
        self.player_names = {1: "GPT-4o", 2: "GPT-4o-mini"}
        
    def display_game_state(self):
        """Display current game state"""
        print("\n" + "="*70)
        print(f"🤖 AI vs AI 成语接龙对战 - 第 {self.round_count + 1}/{self.max_rounds} 轮")
        print(f"📊 分数 - {self.player_names[1]}: {self.scores[1]} | {self.player_names[2]}: {self.scores[2]}")
        print("📜 规则: 成语的最后一个字必须与下一个成语的第一个字相同")
        print("="*70)
        
        if self.game_history:
            print(f"📖 游戏历史: {' -> '.join(self.game_history[-8:])}")  # Show last 8 idioms
            if len(self.game_history) > 8:
                print(f"    ... 还有 {len(self.game_history) - 8} 个成语")
        
        if self.current_idiom:
            print(f"🎯 当前成语: {self.current_idiom}")
            print(f"💡 提示: 下一个成语必须以 '{self.current_idiom[-1]}' 开头")
        print()
    
    def setup_game(self):
        """Setup game with starting idiom"""
        print("🤖 AI vs AI 成语接龙对战! 🤖")
        print("🔹 游戏规则:")
        print("  - 每个成语必须是四个汉字")
        print("  - 成语的第一个字必须与上一个成语的最后一个字相同")
        print("  - 不能重复使用已经说过的成语")
        print("  - 必须是真实存在的中文成语")
        
        # Set starting idiom
        starting_idioms = ["一心一意", "风调雨顺", "龙飞凤舞", "花好月圆", "春回大地"]
        import random
        start_idiom = random.choice(starting_idioms)
        
        self.current_idiom = start_idiom
        self.game_history.append(start_idiom)
        
        print(f"🎯 开始成语: {start_idiom}")
        
        return True
    
    def play_round(self, current_player):
        """Play one round for the specified AI player"""
        self.display_game_state()
        
        player_name = self.player_names[current_player]
        model = PLAYER_MODELS[current_player]
        
        print(f"🤖 {player_name} 正在思考...")
        time.sleep(2)  # Simulate thinking time
        
        idiom = get_ai_idiom(self.game_history, self.current_idiom, model)
        
        if idiom is None:
            print(f"🤖 {player_name} 找不到合适的成语!")
            other_player = 2 if current_player == 1 else 1
            self.scores[other_player] += 5  # Bonus points for opponent
            return False
        
        # Validate AI's idiom
        if not validate_idiom_chain(self.current_idiom, idiom):
            print(f"🤖 {player_name} 出的成语无效: {idiom}")
            other_player = 2 if current_player == 1 else 1
            self.scores[other_player] += 5
            return False
        
        # Check for repeated idiom
        if idiom in self.game_history:
            print(f"🤖 {player_name} 重复了成语: {idiom}")
            other_player = 2 if current_player == 1 else 1
            self.scores[other_player] += 5
            return False
        
        # Valid move
        self.current_idiom = idiom
        self.game_history.append(idiom)
        self.scores[current_player] += 1
        print(f"🤖 {player_name} 出的成语: {idiom}")
        
        self.round_count += 1
        return True
    
    def show_final_score(self):
        """Display final game results"""
        print("\n" + "="*70)
        print("🏆 AI 对战结果 🏆")
        print("="*70)
        print(f"📊 最终分数:")
        print(f"   🤖 {self.player_names[1]}: {self.scores[1]} 分")
        print(f"   🤖 {self.player_names[2]}: {self.scores[2]} 分")
        
        if self.scores[1] > self.scores[2]:
            print(f"\n🎉 {self.player_names[1]} 获胜! 🎉")
        elif self.scores[2] > self.scores[1]:
            print(f"\n🎉 {self.player_names[2]} 获胜! 🎉")
        else:
            print("\n🤝 平局! 两个AI表现相当! 🤝")
        
        print(f"\n📖 完整游戏历史 ({len(self.game_history)} 个成语):")
        for i, idiom in enumerate(self.game_history):
            if i == 0:
                print(f"   🎯 开始成语: {idiom}")
            else:
                player_num = 1 if (i - 1) % 2 == 0 else 2
                player_name = self.player_names[player_num]
                print(f"   {i:2d}. 🤖 {player_name}: {idiom}")
        
        print(f"\n📊 游戏统计:")
        print(f"    成语总数: {len(self.game_history)}")
        print(f"   🔄 对战轮数: {self.round_count}")
        
        # Calculate win rate
        if self.round_count > 0:
            p1_rate = (self.scores[1] / (self.scores[1] + self.scores[2])) * 100 if (self.scores[1] + self.scores[2]) > 0 else 0
            p2_rate = 100 - p1_rate
            print(f"   📈 {self.player_names[1]} 胜率: {p1_rate:.1f}%")
            print(f"   📈 {self.player_names[2]} 胜率: {p2_rate:.1f}%")
        
        print("\n🎮 感谢观看AI成语接龙对战! 🎮")

def main():
    """Main game function"""
    # Parse command line arguments
    max_rounds = MAX_ROUNDS
    if len(sys.argv) > 1:
        try:
            max_rounds = int(sys.argv[1])
            if max_rounds <= 0:
                print("错误: 最大轮数必须是正整数.")
                return
            print(f"🎮 自定义最大轮数: {max_rounds}")
        except ValueError:
            print("错误: 无效的最大轮数参数. 使用默认值.")
    
    print("🤖 成语接龙游戏 - AI vs AI 对战 🤖")
    print("=" * 50)
    
    if not initialize_client_manually():
        print("无法初始化OpenAI客户端. 游戏无法开始.")
        return
    
    game = AIIdiomChainGame(max_rounds)
    
    if not game.setup_game():
        return
    
    print(f"\n🎮 AI对战开始!")
    print(f"🤖 {game.player_names[1]} vs {game.player_names[2]}")
    print(f"🎯 开始成语: {game.current_idiom}")
    print(f"🎲 最大轮数: {game.max_rounds}")
    print("\n让对战开始! 🚀")
    
    # Game loop - alternating turns
    current_player = 1  # Start with Player 1
    
    while game.round_count < game.max_rounds:
        if not game.play_round(current_player):
            break
        current_player = 2 if current_player == 1 else 1  # Switch players
        
        if game.round_count >= game.max_rounds:
            print("\n⏰ 已达到最大轮数!")
            break
    
    game.show_final_score()

if __name__ == "__main__":
    main()
