import random
import time
import sys
import os
import argparse

from splendor_ai_player import initialize_client_manually, client

# Define constants for gem types
GEM_TYPES = ["Diamond", "Sapphire", "Emerald", "Ruby", "Onyx", "Gold"]

class Player:
    def __init__(self, name):
        self.name = name
        self.gems = {gem: 0 for gem in GEM_TYPES}  # Player's gem tokens
        self.cards = []  # Purchased development cards
        self.nobles = []  # Nobles visited
        self.score = 0  # Player's total score

    def __str__(self):
        return str(self.name)  # Ensure __str__ always returns a string

    def take_gems(self, gems):
        """Take gems from the bank."""
        for gem, count in gems.items():
            self.gems[gem] += count

    def buy_card(self, card):
        """Buy a development card."""
        for gem, cost in card['cost'].items():
            self.gems[gem] -= cost
        self.cards.append(card)
        self.score += card['points']

    def reserve_card(self, card):
        """Reserve a development card."""
        self.gems["Gold"] += 1
        # Reserved cards can be stored separately if needed

class LLMPlayer(Player):
    def __init__(self, name, model_name):
        super().__init__(name)
        self.model_name = model_name

    def __str__(self):
        return f"{self.name} ({self.model_name})"  # Include model name for clarity

    def get_action(self, game_state):
        """Ask the LLM to decide its action based on the current game state."""
        if not client:
            print("OpenAI client is not initialized.")
            if not initialize_client_manually():
                return None

        prompt = (
            f"You are an expert Splendor player. The current game state is as follows:\n"
            f"{game_state}\n"
            "You can choose one of the following actions:\n"
            "1. Take gems (specify which gems).\n"
            "2. Reserve a card (specify which card).\n"
            "3. Buy a card (specify which card).\n"
            "Respond with your action in the format: 'Action: [details]'."
        )

        try:
            completion = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful but strict Splendor assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=50,
            )

            response_text = completion.choices[0].message.content.strip()
            print(f"{self.name} ({self.model_name}) responded: '{response_text}'")
            return response_text

        except Exception as e:
            print(f"An error occurred while calling the OpenAI API: {e}")
            return None

class SplendorGame:
    def __init__(self, players, max_rounds=30):
        self.players = [Player(name) for name in players]
        self.gem_bank = {gem: 7 for gem in GEM_TYPES}  # Initial gem counts
        self.gem_bank["Gold"] = 5  # Gold has fewer tokens
        self.cards = self.generate_cards()  # Development cards
        self.nobles = self.generate_nobles()  # Noble tiles
        self.current_player_index = 0
        self.rounds_played = 0  # Track the total number of rounds played
        self.max_rounds = max_rounds  # Maximum number of rounds, now configurable

    def generate_cards(self):
        """Generate development cards."""
        # Example cards, should be replaced with actual game data
        return [
            {"level": 1, "cost": {"Diamond": 1, "Sapphire": 1}, "points": 1},
            {"level": 2, "cost": {"Emerald": 3, "Ruby": 2}, "points": 2},
        ]

    def generate_nobles(self):
        """Generate noble tiles."""
        # Example nobles, should be replaced with actual game data
        return [
            {"requirements": {"Diamond": 3, "Sapphire": 3}, "points": 3},
        ]

    def initialize_gem_bank(self, num_players):
        """Initialize the gem bank based on the number of players."""
        gem_counts = {2: 4, 3: 5, 4: 7}  # Gem counts based on player count
        if num_players not in gem_counts:
            raise ValueError("Invalid number of players. Must be 2, 3, or 4.")

        self.gem_bank = {gem: gem_counts[num_players] for gem in GEM_TYPES if gem != "Gold"}
        self.gem_bank["Gold"] = 5  # Gold is always 5

    def take_gems(self, player, gems):
        """Handle the logic for a player taking gems."""
        print(f"Attempting to take gems: {gems}")
        print("Current gem bank:", self.gem_bank)

        if len(gems) == 3:
            # Check if all selected gems are different and available
            if len(set(gems)) != 3:
                raise ValueError("Invalid gem selection: must select 3 different gems.")
            if not all(self.gem_bank[gem] > 0 for gem in gems):
                unavailable_gems = [gem for gem in gems if self.gem_bank[gem] <= 0]
                raise ValueError(f"Invalid gem selection: gems {unavailable_gems} are not available.")
            # Take 3 different gems
            for gem in gems:
                self.gem_bank[gem] -= 1
                player.gems[gem] += 1
        elif len(gems) == 1:
            # Check if the selected gem has at least 4 available
            if self.gem_bank[gems[0]] < 4:
                raise ValueError(f"Invalid gem selection: must select a gem with at least 4 available to take 2. {gems[0]} has {self.gem_bank[gems[0]]}.")
            # Take 2 of the same gem
            self.gem_bank[gems[0]] -= 2
            player.gems[gems[0]] += 2
        else:
            raise ValueError("Invalid gem selection: must select either 3 different gems or 2 of the same gem.")

        # Enforce gem limit (10 gems max)
        total_gems = sum(player.gems.values())
        if total_gems > 10:
            excess = total_gems - 10
            print(f"{player.name} has {total_gems} gems, returning {excess} gems.")
            self.return_excess_gems(player, excess)

        print(f"{player.name} successfully took gems: {gems}")
        print("Updated gem bank:", self.gem_bank)
        print(f"{player.name}'s gems:", player.gems)

    def return_excess_gems(self, player, excess):
        """Return excess gems to the bank."""
        returned = 0
        for gem, count in player.gems.items():
            if returned >= excess:
                break
            if count > 0:
                to_return = min(count, excess - returned)
                player.gems[gem] -= to_return
                self.gem_bank[gem] += to_return
                returned += to_return
        print(f"{player.name} returned {returned} excess gems.")

    def buy_card(self, player, card):
        """Handle the logic for a player buying a development card."""
        # Check if the player can afford the card
        for gem, cost in card['cost'].items():
            available = player.gems[gem] + sum(c['gem'] == gem for c in player.cards)
            if available < cost:
                raise ValueError(f"{player.name} cannot afford this card.")

        # Deduct the cost
        for gem, cost in card['cost'].items():
            while cost > 0:
                if player.gems[gem] > 0:
                    player.gems[gem] -= 1
                    cost -= 1
                elif player.gems["Gold"] > 0:
                    player.gems["Gold"] -= 1
                    cost -= 1

        # Add the card to the player's collection
        player.cards.append(card)
        player.score += card['points']

        # Replenish the card on the table
        self.replenish_card(card)

    def replenish_card(self, card):
        """Replenish the card on the table from the corresponding deck."""
        level = card['level']
        # Logic to draw a new card from the deck (to be implemented)
        print(f"Replenished a card of level {level}.")

    def check_game_end(self):
        """Check if the game has ended."""
        for player in self.players:
            if player.score >= 15:
                print(f"Game end triggered by {player.name} with {player.score} points.")
                return True
        return False

    def generate_ai_action(self, player):
        """Generate a valid action for the AI player."""
        # Check available gems in the gem bank
        available_gems = [gem for gem, count in self.gem_bank.items() if count > 0 and gem != "Gold"]

        # Try to take 3 different gems if possible
        if len(available_gems) >= 3:
            return {"action": "take_gems", "gems": available_gems[:3]}

        # Try to take 2 of the same gem if possible
        for gem in available_gems:
            if self.gem_bank[gem] >= 4:
                return {"action": "take_gems", "gems": [gem]}

        # Try to buy a card if possible
        for card in self.cards:
            if self.can_afford_card(player, card):
                return {"action": "buy_card", "card": card}

        # Try to reserve a card if possible
        if len(player.cards) < 3:
            for card in self.cards:
                return {"action": "reserve_card", "card": card}

        # If the player already has 3 reserved cards, discard the oldest and reserve a new one
        if len(player.cards) == 3:
            discarded_card = player.cards.pop(0)  # Discard the oldest reserved card
            print(f"{player.name} discarded a reserved card: {discarded_card}")
            for card in self.cards:
                return {"action": "reserve_card", "card": card}

        # No valid action possible, skip turn
        print(f"{player.name} skips their turn due to no valid actions. Debug Info: Gems: {player.gems}, Cards: {len(player.cards)}, Gem Bank: {self.gem_bank}")
        return {"action": "skip"}

    def can_afford_card(self, player, card):
        """Check if the player can afford a card."""
        for gem, cost in card['cost'].items():
            # Calculate available gems including bonuses from cards
            bonus = sum(1 for c in player.cards if c.get('bonus') == gem)
            available = player.gems[gem] + bonus
            if available < cost:
                return False
        return True

    def take_gems(self, player, gems):
        """Handle the logic for a player taking gems."""
        print(f"Attempting to take gems: {gems}")
        print("Current gem bank:", self.gem_bank)

        if len(gems) == 3:
            # Check if all selected gems are different and available
            if len(set(gems)) != 3:
                raise ValueError("Invalid gem selection: must select 3 different gems.")
            if not all(self.gem_bank[gem] > 0 for gem in gems):
                unavailable_gems = [gem for gem in gems if self.gem_bank[gem] <= 0]
                raise ValueError(f"Invalid gem selection: gems {unavailable_gems} are not available.")
            # Take 3 different gems
            for gem in gems:
                self.gem_bank[gem] -= 1
                player.gems[gem] += 1
        elif len(gems) == 1:
            # Check if the selected gem has at least 4 available
            if self.gem_bank[gems[0]] < 4:
                raise ValueError(f"Invalid gem selection: must select a gem with at least 4 available to take 2. {gems[0]} has {self.gem_bank[gems[0]]}.")
            # Take 2 of the same gem
            self.gem_bank[gems[0]] -= 2
            player.gems[gems[0]] += 2
        else:
            raise ValueError("Invalid gem selection: must select either 3 different gems or 2 of the same gem.")

        # Enforce gem limit (10 gems max)
        total_gems = sum(player.gems.values())
        if total_gems > 10:
            excess = total_gems - 10
            print(f"{player.name} has {total_gems} gems, returning {excess} gems.")
            self.return_excess_gems(player, excess)

        print(f"{player.name} successfully took gems: {gems}")
        print("Updated gem bank:", self.gem_bank)
        print(f"{player.name}'s gems:", player.gems)

    def return_excess_gems(self, player, excess):
        """Return excess gems to the bank."""
        returned = 0
        for gem, count in player.gems.items():
            if returned >= excess:
                break
            if count > 0:
                to_return = min(count, excess - returned)
                player.gems[gem] -= to_return
                self.gem_bank[gem] += to_return
                returned += to_return
        print(f"{player.name} returned {returned} excess gems.")

    def buy_card(self, player, card):
        """Handle the logic for a player buying a development card."""
        # Check if the player can afford the card
        for gem, cost in card['cost'].items():
            available = player.gems[gem] + sum(c['gem'] == gem for c in player.cards)
            if available < cost:
                raise ValueError(f"{player.name} cannot afford this card.")

        # Deduct the cost
        for gem, cost in card['cost'].items():
            while cost > 0:
                if player.gems[gem] > 0:
                    player.gems[gem] -= 1
                    cost -= 1
                elif player.gems["Gold"] > 0:
                    player.gems["Gold"] -= 1
                    cost -= 1

        # Add the card to the player's collection
        player.cards.append(card)
        player.score += card['points']

        # Replenish the card on the table
        self.replenish_card(card)

    def replenish_card(self, card):
        """Replenish the card on the table from the corresponding deck."""
        level = card['level']
        # Logic to draw a new card from the deck (to be implemented)
        print(f"Replenished a card of level {level}.")

    def check_game_end(self):
        """Check if the game has ended."""
        for player in self.players:
            if player.score >= 15:
                print(f"Game end triggered by {player.name} with {player.score} points.")
                return True
        return False

    def generate_ai_action(self, player):
        """Generate a valid action for the AI player."""
        # Check available gems in the gem bank
        available_gems = [gem for gem, count in self.gem_bank.items() if count > 0 and gem != "Gold"]

        # Try to take 3 different gems if possible
        if len(available_gems) >= 3:
            return {"action": "take_gems", "gems": available_gems[:3]}

        # Try to take 2 of the same gem if possible
        for gem in available_gems:
            if self.gem_bank[gem] >= 4:
                return {"action": "take_gems", "gems": [gem]}

        # Try to buy a card if possible
        for card in self.cards:
            if self.can_afford_card(player, card):
                return {"action": "buy_card", "card": card}

        # Try to reserve a card if possible
        if len(player.cards) < 3:
            for card in self.cards:
                return {"action": "reserve_card", "card": card}

        # If the player already has 3 reserved cards, discard the oldest and reserve a new one
        if len(player.cards) == 3:
            discarded_card = player.cards.pop(0)  # Discard the oldest reserved card
            print(f"{player.name} discarded a reserved card: {discarded_card}")
            for card in self.cards:
                return {"action": "reserve_card", "card": card}

        # No valid action possible, skip turn
        print(f"{player.name} skips their turn due to no valid actions. Debug Info: Gems: {player.gems}, Cards: {len(player.cards)}, Gem Bank: {self.gem_bank}")
        return {"action": "skip"}

    def can_afford_card(self, player, card):
        """Check if the player can afford a card."""
        for gem, cost in card['cost'].items():
            # Calculate available gems including bonuses from cards
            bonus = sum(1 for c in player.cards if c.get('bonus') == gem)
            available = player.gems[gem] + bonus
            if available < cost:
                return False
        return True

    def play_turn(self):
        """Play a single turn for the current player."""
        player = self.players[self.current_player_index]
        print(f"{str(player)}'s turn")  # Ensure player name is displayed correctly

        start_time = time.time()

        if isinstance(player, LLMPlayer):
            game_state = format_game_state(self)
            action = player.get_action(game_state)
            print(f"LLM action: {action}")
            # Parse and execute the action
            if action and action.startswith("Action:"):
                try:
                    action_type, details = action.split(":", 1)
                    action_type = action_type.strip().lower()
                    details = details.strip()

                    if action_type == "take gems":
                        gems = [gem.strip() for gem in details.split(",")]
                        self.take_gems(player, gems)
                    elif action_type == "buy card":
                        card_index = int(details)  # Assuming card index is provided
                        self.buy_card(player, self.cards[card_index])
                    elif action_type == "reserve card":
                        card_index = int(details)  # Assuming card index is provided
                        self.reserve_card(player, self.cards[card_index])
                    else:
                        print(f"Unknown action type: {action_type}")
                except Exception as e:
                    print(f"Failed to parse or execute action: {e}")
        else:
            # Generate a valid action for AI players
            ai_action = self.generate_ai_action(player)
            if ai_action["action"] == "take_gems":
                try:
                    self.take_gems(player, ai_action["gems"])
                except ValueError as e:
                    print(f"Failed to take gems: {e}")
            elif ai_action["action"] == "buy_card":
                self.buy_card(player, ai_action["card"])
            elif ai_action["action"] == "reserve_card":
                self.reserve_card(player, ai_action["card"])
            elif ai_action["action"] == "skip":
                print(f"{player.name} skips their turn due to no valid actions.")

        # Enforce a time limit of 1-5 seconds per turn
        elapsed_time = time.time() - start_time
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)
        elif elapsed_time > 5:
            print(f"{player.name} took too long! Turn skipped.")

        # Display the player's current score
        print(f"{player.name}'s current score: {player.score}")

        # Move to the next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        # Check if a full round is completed
        if self.current_player_index == 0:
            self.rounds_played += 1
            print(f"Round {self.rounds_played} completed.")
            # Display scores for all players
            print("Scores after this round:")
            for p in self.players:
                print(f"{p.name}: {p.score} points")

        # Debugging: Print current gem bank and player gems
        print("Current gem bank:", self.gem_bank)
        print(f"{player.name}'s gems:", player.gems)

    def reserve_card(self, player, card):
        """Handle the logic for a player reserving a development card."""
        if len(player.cards) >= 3:
            raise ValueError(f"{player.name} cannot reserve more than 3 cards.")

        # Add the card to the player's reserved cards
        player.cards.append(card)

        # Remove the card from the available cards
        self.cards.remove(card)

        # Give the player a gold token if available
        if self.gem_bank["Gold"] > 0:
            self.gem_bank["Gold"] -= 1
            player.gems["Gold"] += 1

        print(f"{player.name} reserved a card: {card}")

    def play_game(self):
        """Run the game loop."""
        while not self.check_game_end() and self.rounds_played < self.max_rounds:
            self.play_turn()

        if self.rounds_played >= self.max_rounds:
            print("Game over! Maximum rounds reached. The game is a draw.")
        else:
            # Determine the winner
            winner = max(self.players, key=lambda p: p.score)
            print(f"Game over! The winner is {winner.name} with {winner.score} points.")

def format_game_state(game):
    """Format the current game state for LLMs."""
    state = "Gem Bank:\n" + ", ".join(f"{gem}: {count}" for gem, count in game.gem_bank.items()) + "\n\n"
    state += "Players:\n"
    for player in game.players:
        state += f"{player.name} - Score: {player.score}, Gems: {player.gems}, Cards: {len(player.cards)}, Nobles: {len(player.nobles)}\n"
    return state

class SplendorGameWithLLMs(SplendorGame):
    def play_turn(self):
        """Play a single turn for the current player."""
        player = self.players[self.current_player_index]
        print(f"{str(player)}'s turn")  # Ensure player name is displayed correctly

        if isinstance(player, LLMPlayer):
            game_state = format_game_state(self)
            action = player.get_action(game_state)
            # Parse and execute the action (to be implemented)
            print(f"LLM action: {action}")
        else:
            super().play_turn()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a Splendor game.")
    parser.add_argument(
        "--max_rounds", type=int, default=30, help="Maximum number of rounds for the game (default: 30)"
    )
    args = parser.parse_args()

    players = [
        LLMPlayer("GPT-4o", "gpt-4o"),
        LLMPlayer("GPT-4o-mini", "gpt-4o-mini"),
        LLMPlayer("GPT-4.1-mini", "gpt-4.1-mini"),
        LLMPlayer("GPT-4.1-nano", "gpt-4.1-nano")
    ]
    game = SplendorGameWithLLMs(players=players, max_rounds=args.max_rounds)
    game.play_game()
