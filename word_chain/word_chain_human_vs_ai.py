import time
import sys
from ai_player import get_ai_idiom, initialize_client_manually, validate_idiom_chain

MAX_ROUNDS = 100
PLAYER_MODELS = {"ai": "gpt-4o"}  # AI as the opponent

class IdiomChainGame:
    def __init__(self, max_rounds=MAX_ROUNDS):
        self.game_history = []
        self.current_idiom = ""
        self.round_count = 0
        self.max_rounds = max_rounds
        self.scores = {"human": 0, "ai": 0}
        
    def display_game_state(self):
        """Display current game state"""
        print("\n" + "="*60)
        print(f"🎯 成语接龙游戏 - 第 {self.round_count + 1}/{self.max_rounds} 轮")
        print(f"📊 分数 - 人类: {self.scores['human']} | AI: {self.scores['ai']}")
        print("📜 规则: 成语的最后一个字必须与下一个成语的第一个字相同")
        print("="*60)
        
        if self.game_history:
            print(f"📖 游戏历史: {' -> '.join(self.game_history[-10:])}")  # Show last 10 idioms
            if len(self.game_history) > 10:
                print(f"    ... 还有 {len(self.game_history) - 10} 个成语")
        
        if self.current_idiom:
            print(f"🎯 当前成语: {self.current_idiom}")
            print(f"💡 提示: 下一个成语必须以 '{self.current_idiom[-1]}' 开头")
        print()
    
    def setup_game(self):
        """Setup game with starting idiom"""
        print("🎮 欢迎来到成语接龙游戏! 🎮")
        print("🔹 游戏规则:")
        print("  - 每个成语必须是四个汉字")
        print("  - 你的成语的第一个字必须与上一个成语的最后一个字相同")
        print("  - 不能重复使用已经说过的成语")
        print("  - 必须是真实存在的中文成语")
        
        # Get starting idiom
        while True:
            try:
                start_idiom = input("请输入开始的成语(四个汉字): ").strip()
                
                # Validate it's a 4-character Chinese idiom
                if len(start_idiom) == 4 and all('\u4e00' <= char <= '\u9fff' for char in start_idiom):
                    self.current_idiom = start_idiom
                    self.game_history.append(start_idiom)
                    break
                else:
                    print("请输入一个四字成语(只能包含汉字).")
            except KeyboardInterrupt:
                print("\n游戏取消.")
                return False
        
        return True
    
    def get_human_idiom(self):
        """Get idiom from human player"""
        while True:
            try:
                user_input = input("请输入你的成语 (输入 'quit' 退出): ").strip()
                
                if user_input.lower() == 'quit':
                    return None
                
                if not user_input:
                    print("请输入一个成语.")
                    continue
                
                # Validate it's a 4-character Chinese idiom
                if len(user_input) != 4 or not all('\u4e00' <= char <= '\u9fff' for char in user_input):
                    print("请输入一个四字成语(只能包含汉字).")
                    continue
                
                if user_input in self.game_history:
                    print("这个成语已经使用过了. 请选择另一个成语.")
                    continue
                
                # Validate idiom chain rule
                if not validate_idiom_chain(self.current_idiom, user_input):
                    print(f"成语不符合接龙规则. 你的成语必须以 '{self.current_idiom[-1]}' 开头. 请重试.")
                    continue
                
                return user_input
                
            except KeyboardInterrupt:
                print("\n游戏取消.")
                return None
    
    def play_round(self, human_turn=True):
        """Play one round of the game"""
        self.display_game_state()
        
        if human_turn:
            print("👤 轮到你了!")
            idiom = self.get_human_idiom()
            if idiom is None:
                return False  # Game ended
            
            self.current_idiom = idiom
            self.game_history.append(idiom)
            self.scores["human"] += 1
            print(f"✅ 你出的成语: {idiom}")
            
        else:
            print("🤖 AI正在思考...")
            time.sleep(1)  # Simulate thinking time
            
            idiom = get_ai_idiom(self.game_history, self.current_idiom, PLAYER_MODELS["ai"])
            
            if idiom is None:
                print("🤖 AI找不到合适的成语. 你赢了这一轮!")
                self.scores["human"] += 5  # Bonus points for AI failure
                return False
            
            # Validate AI's idiom
            if not validate_idiom_chain(self.current_idiom, idiom):
                print(f"🤖 AI出的成语无效: {idiom}. 你赢了这一轮!")
                self.scores["human"] += 5
                return False
            
            if idiom in self.game_history:
                print(f"🤖 AI重复了成语: {idiom}. 你赢了这一轮!")
                self.scores["human"] += 5
                return False
            
            self.current_idiom = idiom
            self.game_history.append(idiom)
            self.scores["ai"] += 1
            print(f"🤖 AI出的成语: {idiom}")
        
        self.round_count += 1
        return True
    
    def show_final_score(self):
        """Display final game results"""
        print("\n" + "="*60)
        print("🏆 游戏结束 🏆")
        print("="*60)
        print(f"📊 最终分数:")
        print(f"   👤 人类: {self.scores['human']} 分")
        print(f"   🤖 AI: {self.scores['ai']} 分")
        
        if self.scores['human'] > self.scores['ai']:
            print("\n🎉 恭喜你获胜! 🎉")
        elif self.scores['ai'] > self.scores['human']:
            print("\n🤖 AI获胜! 下次继续努力! 🤖")
        else:
            print("\n🤝 平局! 精彩的游戏! 🤝")
        
        print(f"\n📖 完整游戏历史 ({len(self.game_history)} 个成语):")
        for i, idiom in enumerate(self.game_history, 1):
            player = "👤" if i % 2 == 1 else "🤖"
            print(f"   {i:2d}. {player} {idiom}")
        
        print("\n🎮 感谢游玩成语接龙游戏! 🎮")

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
    
    print("🎯 成语接龙游戏 - 人类 vs AI 🤖")
    print("=" * 50)
    
    if not initialize_client_manually():
        print("无法初始化OpenAI客户端. 游戏无法开始.")
        return
    
    game = IdiomChainGame(max_rounds)
    
    if not game.setup_game():
        return
    
    print(f"\n🎮 成语接龙游戏开始!")
    print(f"🎯 开始成语: {game.current_idiom}")
    print(f"🎲 最大轮数: {game.max_rounds}")
    print("\n开始游戏! 🚀")
    
    # Game loop - alternating turns
    human_turn = True  # Human starts after the initial idiom
    
    while game.round_count < game.max_rounds:
        if not game.play_round(human_turn):
            break
        human_turn = not human_turn  # Switch turns
        
        if game.round_count >= game.max_rounds:
            print("\n⏰ 已达到最大轮数!")
            break
    
    game.show_final_score()

if __name__ == "__main__":
    main()
