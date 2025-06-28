import time
import sys
from ai_player import get_ai_word, initialize_client_manually, validate_word_chain

MAX_ROUNDS = 100
PLAYER_MODELS = {"ai": "gpt-4o"}  # AI as the opponent

class WordChainGame:
    def __init__(self, max_rounds=MAX_ROUNDS):
        self.game_history = []
        self.current_word = ""
        self.rule_type = ""
        self.round_count = 0
        self.max_rounds = max_rounds
        self.scores = {"human": 0, "ai": 0}
        
    def display_game_state(self):
        """Display current game state"""
        print("\n" + "="*60)
        print(f"🎯 Word Chain Game - Round {self.round_count + 1}/{self.max_rounds}")
        print(f"📊 Score - Human: {self.scores['human']} | AI: {self.scores['ai']}")
        print(f"📜 Rule: {self.get_rule_description()}")
        print("="*60)
        
        if self.game_history:
            print(f"📖 Game History: {' -> '.join(self.game_history[-10:])}")  # Show last 10 words
            if len(self.game_history) > 10:
                print(f"    ... and {len(self.game_history) - 10} more words")
        
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
        print("🎮 Welcome to Word Chain Game! 🎮")
        print("Choose your game rule:")
        print("1. Tail-to-Head (首尾相接) - First character matches last character")
        print("2. Same Category (同类词语) - Words must be in the same category")
        print("3. Mixed Rules (混合规则) - Either rule above works")
        
        while True:
            try:
                choice = input("Enter your choice (1-3): ").strip()
                if choice == "1":
                    self.rule_type = "tail_to_head"
                    break
                elif choice == "2":
                    self.rule_type = "category"
                    break
                elif choice == "3":
                    self.rule_type = "mixed"
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except KeyboardInterrupt:
                print("\nGame cancelled.")
                return False
        
        # Get starting word
        while True:
            try:
                start_word = input("Enter the starting word/phrase: ").strip()
                if start_word and len(start_word) <= 20:
                    self.current_word = start_word
                    self.game_history.append(start_word)
                    break
                else:
                    print("Please enter a valid word (1-20 characters).")
            except KeyboardInterrupt:
                print("\nGame cancelled.")
                return False
        
        return True
    
    def get_human_word(self):
        """Get word from human player"""
        while True:
            try:
                user_input = input("Enter your word (or 'quit' to exit): ").strip()
                
                if user_input.lower() == 'quit':
                    return None
                
                if not user_input:
                    print("Please enter a word.")
                    continue
                
                if len(user_input) > 20:
                    print("Word too long. Please enter a shorter word (max 20 characters).")
                    continue
                
                if user_input in self.game_history:
                    print("This word has already been used. Please choose a different word.")
                    continue
                
                # Validate word chain rule
                if not validate_word_chain(self.current_word, user_input, self.rule_type):
                    print(f"Word doesn't follow the {self.get_rule_description()} rule. Please try again.")
                    if self.rule_type == 'tail_to_head':
                        print(f"Hint: Your word should start with '{self.current_word[-1]}'")
                    continue
                
                return user_input
                
            except KeyboardInterrupt:
                print("\nGame cancelled.")
                return None
    
    def play_round(self, human_turn=True):
        """Play one round of the game"""
        self.display_game_state()
        
        if human_turn:
            print("👤 Your turn!")
            word = self.get_human_word()
            if word is None:
                return False  # Game ended
            
            self.current_word = word
            self.game_history.append(word)
            self.scores["human"] += 1
            print(f"✅ You played: {word}")
            
        else:
            print("🤖 AI is thinking...")
            time.sleep(1)  # Simulate thinking time
            
            word = get_ai_word(self.game_history, self.current_word, self.rule_type, PLAYER_MODELS["ai"])
            
            if word is None:
                print("🤖 AI couldn't find a valid word. You win this round!")
                self.scores["human"] += 5  # Bonus points for AI failure
                return False
            
            # Validate AI's word
            if not validate_word_chain(self.current_word, word, self.rule_type):
                print(f"🤖 AI played an invalid word: {word}. You win this round!")
                self.scores["human"] += 5
                return False
            
            if word in self.game_history:
                print(f"🤖 AI repeated a word: {word}. You win this round!")
                self.scores["human"] += 5
                return False
            
            self.current_word = word
            self.game_history.append(word)
            self.scores["ai"] += 1
            print(f"🤖 AI played: {word}")
        
        self.round_count += 1
        return True
    
    def show_final_score(self):
        """Display final game results"""
        print("\n" + "="*60)
        print("🏆 GAME OVER 🏆")
        print("="*60)
        print(f"📊 Final Score:")
        print(f"   👤 Human: {self.scores['human']} points")
        print(f"   🤖 AI: {self.scores['ai']} points")
        
        if self.scores['human'] > self.scores['ai']:
            print("\n🎉 Congratulations! You won! 🎉")
        elif self.scores['ai'] > self.scores['human']:
            print("\n🤖 AI wins! Better luck next time! 🤖")
        else:
            print("\n🤝 It's a tie! Great game! 🤝")
        
        print(f"\n📖 Complete Game History ({len(self.game_history)} words):")
        for i, word in enumerate(self.game_history, 1):
            player = "👤" if i % 2 == 1 else "🤖"
            print(f"   {i:2d}. {player} {word}")
        
        print("\n🎮 Thanks for playing Word Chain Game! 🎮")

def main():
    """Main game function"""
    # Parse command line arguments
    max_rounds = MAX_ROUNDS
    if len(sys.argv) > 1:
        try:
            max_rounds = int(sys.argv[1])
            if max_rounds <= 0:
                print("Error: Maximum rounds must be a positive integer.")
                return
            print(f"🎮 Custom max rounds: {max_rounds}")
        except ValueError:
            print("Error: Invalid max rounds argument. Using default value.")
    
    print("🎯 Word Chain Game - Human vs AI 🤖")
    print("=" * 50)
    
    if not initialize_client_manually():
        print("Unable to initialize OpenAI client. Game cannot start.")
        return
    
    game = WordChainGame(max_rounds)
    
    if not game.setup_game():
        return
    
    print(f"\n🎮 Game started with rule: {game.get_rule_description()}")
    print(f"🎯 Starting word: {game.current_word}")
    print(f"🎲 Maximum rounds: {game.max_rounds}")
    print("\nLet's play! 🚀")
    
    # Game loop - alternating turns
    human_turn = True  # Human starts after the initial word
    
    while game.round_count < game.max_rounds:
        if not game.play_round(human_turn):
            break
        human_turn = not human_turn  # Switch turns
        
        if game.round_count >= game.max_rounds:
            print("\n⏰ Maximum rounds reached!")
            break
    
    game.show_final_score()

if __name__ == "__main__":
    main()
