import time
from ai_player import get_ai_word, initialize_client_manually, validate_word_chain

MAX_ROUNDS = 30
PLAYER_MODELS = {
    1: "gpt-4o",
    2: "gpt-4o-mini"
}

class AIWordChainGame:
    def __init__(self):
        self.game_history = []
        self.current_word = ""
        self.rule_type = ""
        self.round_count = 0
        self.scores = {1: 0, 2: 0}
        self.player_names = {1: "GPT-4o", 2: "GPT-4o-mini"}
        
    def display_game_state(self):
        """Display current game state"""
        print("\n" + "="*70)
        print(f"🤖 AI vs AI Word Chain Battle - Round {self.round_count + 1}/{MAX_ROUNDS}")
        print(f"📊 Score - {self.player_names[1]}: {self.scores[1]} | {self.player_names[2]}: {self.scores[2]}")
        print(f"📜 Rule: {self.get_rule_description()}")
        print("="*70)
        
        if self.game_history:
            print(f"📖 Game History: {' -> '.join(self.game_history[-8:])}")  # Show last 8 words
            if len(self.game_history) > 8:
                print(f"    ... and {len(self.game_history) - 8} more words")
        
        if self.current_word:
            print(f"🎯 Current Word: {self.current_word}")
        print()
    
    def get_rule_description(self):
        """Get human-readable rule description"""
        rules = {
            'tail_to_head': "Tail-to-Head (首尾相接)",
            'category': "Same Category (同类词语)",
            'mixed': "Mixed Rules (混合规则)"
        }
        return rules.get(self.rule_type, "Unknown")
    
    def setup_game(self):
        """Setup game rules and starting word"""
        print("🤖 AI vs AI Word Chain Battle! 🤖")
        print("Choose game rule:")
        print("1. Tail-to-Head (首尾相接) - First character matches last character")
        print("2. Same Category (同类词语) - Words must be in the same category")
        print("3. Mixed Rules (混合规则) - Either rule above works")
        print("4. Auto-select random rule")
        
        while True:
            try:
                choice = input("Enter your choice (1-4): ").strip()
                if choice == "1":
                    self.rule_type = "tail_to_head"
                    break
                elif choice == "2":
                    self.rule_type = "category"
                    break
                elif choice == "3":
                    self.rule_type = "mixed"
                    break
                elif choice == "4":
                    import random
                    self.rule_type = random.choice(["tail_to_head", "category", "mixed"])
                    print(f"🎲 Randomly selected: {self.get_rule_description()}")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, 3, or 4.")
            except KeyboardInterrupt:
                print("\nGame cancelled.")
                return False
        
        # Set starting word
        starting_words = {
            'tail_to_head': "龙",
            'category': "苹果",
            'mixed': "智慧"
        }
        
        self.current_word = starting_words.get(self.rule_type, "开始")
        self.game_history.append(self.current_word)
        
        return True
    
    def play_round(self, current_player):
        """Play one round for the specified AI player"""
        self.display_game_state()
        
        player_name = self.player_names[current_player]
        model = PLAYER_MODELS[current_player]
        
        print(f"🤖 {player_name} is thinking...")
        time.sleep(2)  # Simulate thinking time
        
        word = get_ai_word(self.game_history, self.current_word, self.rule_type, model)
        
        if word is None:
            print(f"🤖 {player_name} couldn't find a valid word!")
            other_player = 2 if current_player == 1 else 1
            self.scores[other_player] += 5  # Bonus points for opponent
            return False
        
        # Validate AI's word
        if not validate_word_chain(self.current_word, word, self.rule_type):
            print(f"🤖 {player_name} played an invalid word: {word}")
            other_player = 2 if current_player == 1 else 1
            self.scores[other_player] += 5
            return False
        
        if word in self.game_history:
            print(f"🤖 {player_name} repeated a word: {word}")
            other_player = 2 if current_player == 1 else 1
            self.scores[other_player] += 5
            return False
        
        self.current_word = word
        self.game_history.append(word)
        self.scores[current_player] += 1
        
        print(f"🤖 {player_name} played: {word}")
        time.sleep(1)
        
        self.round_count += 1
        return True
    
    def show_final_score(self):
        """Display final game results"""
        print("\n" + "="*70)
        print("🏆 AI BATTLE RESULTS 🏆")
        print("="*70)
        print(f"📊 Final Score:")
        print(f"   🤖 {self.player_names[1]}: {self.scores[1]} points")
        print(f"   🤖 {self.player_names[2]}: {self.scores[2]} points")
        
        if self.scores[1] > self.scores[2]:
            print(f"\n🎉 {self.player_names[1]} wins! 🎉")
        elif self.scores[2] > self.scores[1]:
            print(f"\n🎉 {self.player_names[2]} wins! 🎉")
        else:
            print("\n🤝 It's a tie! Both AIs performed equally well! 🤝")
        
        print(f"\n📖 Complete Game History ({len(self.game_history)} words):")
        for i, word in enumerate(self.game_history):
            if i == 0:
                print(f"   🎯 Starting word: {word}")
            else:
                player_num = 1 if (i - 1) % 2 == 0 else 2
                player_name = self.player_names[player_num]
                print(f"   {i:2d}. 🤖 {player_name}: {word}")
        
        print(f"\n📊 Game Statistics:")
        print(f"   🎮 Rule Used: {self.get_rule_description()}")
        print(f"   🎯 Total Words: {len(self.game_history)}")
        print(f"   🔄 Rounds Played: {self.round_count}")
        
        # Calculate win rate
        if self.round_count > 0:
            p1_rate = (self.scores[1] / (self.scores[1] + self.scores[2])) * 100 if (self.scores[1] + self.scores[2]) > 0 else 0
            p2_rate = 100 - p1_rate
            print(f"   📈 Win Rate - {self.player_names[1]}: {p1_rate:.1f}% | {self.player_names[2]}: {p2_rate:.1f}%")
        
        print("\n🎮 Thanks for watching the AI battle! 🎮")

def main():
    """Main game function"""
    print("🤖 Word Chain Game - AI vs AI Battle 🤖")
    print("=" * 50)
    
    if not initialize_client_manually():
        print("Unable to initialize OpenAI client. Game cannot start.")
        return
    
    game = AIWordChainGame()
    
    if not game.setup_game():
        return
    
    print(f"\n🎮 AI Battle started!")
    print(f"🤖 {game.player_names[1]} vs {game.player_names[2]}")
    print(f"📜 Rule: {game.get_rule_description()}")
    print(f"🎯 Starting word: {game.current_word}")
    print(f"🎲 Maximum rounds: {MAX_ROUNDS}")
    print("\nLet the battle begin! 🚀")
    
    # Game loop - alternating turns
    current_player = 1  # Start with Player 1
    
    while game.round_count < MAX_ROUNDS:
        if not game.play_round(current_player):
            break
        current_player = 2 if current_player == 1 else 1  # Switch players
        
        if game.round_count >= MAX_ROUNDS:
            print("\n⏰ Maximum rounds reached!")
            break
    
    game.show_final_score()

if __name__ == "__main__":
    main()
