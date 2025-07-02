import os
import re
import getpass
from openai import OpenAI

# --- Client Initialization ---
api_key = os.environ.get("OPENAI_API_KEY")  # Use environment variable for API key
client = None

if api_key:
    try:
        client = OpenAI(api_key=api_key)
        print("OpenAI client initialized using environment variable.")
    except Exception as e:
        print(f"Error initializing OpenAI client with environment variable: {e}")
else:
    print("OPENAI_API_KEY environment variable not found.")

def initialize_client_manually():
    global client
    if not client:
        try:
            api_key_manual = getpass.getpass("Please enter your OpenAI API Key: ")
            client = OpenAI(api_key=api_key_manual)
            print("OpenAI client initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize OpenAI client: {e}")
            client = None
    return client is not None

def get_ai_move(board, player, model_name):
    if not client:
        print("OpenAI client is not initialized.")
        if not initialize_client_manually():
            return None

    player_symbol = "X" if player == 1 else "O"
    opponent_symbol = "O" if player == 1 else "X" 
    base_prompt = (
        f"You are an expert Gomoku (Five-in-a-Row) player. You are Player {player} playing as '{player_symbol}'.\n"
        f"Your opponent is playing as '{opponent_symbol}'.\n"
        "The board is a 15x15 grid with coordinates from (0,0) to (14,14).\n"
        f"You MUST choose an empty position marked with '.' to place your '{player_symbol}' piece.\n\n"
        "Current board state:\n"
        f"{board_to_string(board)}\n"
        "IMPORTANT: You must respond with ONLY the coordinates in the format 'row,col' where the position is empty (marked with '.').\n"
    )

    for attempt in range(3): # Retry up to 3 times
        if attempt == 0:
            instruction = "Choose your best move. Respond with ONLY 'row,col' coordinates (e.g., '7,8')."
        elif attempt == 1:
            # Show which positions are already taken
            taken_positions = []
            for i in range(15):
                for j in range(15):
                    if board[i][j] != 0:
                        piece = "X" if board[i][j] == 1 else "O"
                        taken_positions.append(f"({i},{j})={piece}")
            
            instruction = f"INVALID MOVE! You selected an occupied position. Here are all occupied positions: {', '.join(taken_positions)}. Look at the board again and choose ONLY coordinates marked with '.' (dot). Respond ONLY with 'row,col'."
        else:
            instruction = "FINAL ATTEMPT! You must choose an empty position marked with '.' on the board. Any invalid move will result in forfeit. Respond ONLY with 'row,col' coordinates."

        prompt = base_prompt + instruction

        try:
            print(f"\nAsking {model_name} for its move (Attempt {attempt + 1})...")
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful but strict Gomoku assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2 + (attempt * 0.2), # Increase creativity slightly on retries
                max_tokens=15,
            )
            
            response_text = completion.choices[0].message.content.strip()
            print(f"{model_name} responded: '{response_text}'")

            # Updated regex to handle both "X,Y" and "(X, Y)" formats
            match = re.search(r'\(?(\d{1,2}),\s*(\d{1,2})\)?', response_text)
            
            if match:
                row, col = map(int, match.groups())
                if 0 <= row < 15 and 0 <= col < 15:
                    # Final check to ensure the spot is actually empty
                    if board[row][col] == 0:
                        print(f"✓ Valid move at ({row},{col})")
                        return row, col
                    else:
                        occupied_by = "X" if board[row][col] == 1 else "O"
                        print(f"✗ Position ({row},{col}) is occupied by {occupied_by}. Current board[{row}][{col}] = {board[row][col]}")
                        continue # Move to the next attempt
                else:
                    print(f"✗ Coordinates ({row},{col}) are out of bounds (0-14). Retrying...")
            else:
                print(f"✗ Could not parse coordinates from response: '{response_text}'. Expected format: 'row,col'")

        except Exception as e:
            print(f"An error occurred while calling the OpenAI API: {e}")
            # We will retry on API errors as well
    
    print("AI failed to provide a valid move after 3 attempts.")
    return None

def get_ai_action(game_state, player, model_name):
    """Generate an action for the AI player in Splendor."""
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

    for attempt in range(3):  # Retry up to 3 times
        if attempt == 0:
            instruction = "Choose your best move. Respond with ONLY 'Action: [details]'."
        elif attempt == 1:
            instruction = "INVALID ACTION! Ensure your action is valid based on the game state. Respond with ONLY 'Action: [details]'."
        else:
            instruction = "FINAL ATTEMPT! Provide a valid action or your turn will be skipped. Respond with ONLY 'Action: [details]'."

        full_prompt = prompt + "\n" + instruction

        try:
            print(f"\nAsking {model_name} for its action (Attempt {attempt + 1})...")
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful but strict Splendor assistant."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7,
                max_tokens=50,
            )

            response_text = completion.choices[0].message.content.strip()
            print(f"{model_name} responded: '{response_text}'")

            if response_text.startswith("Action:"):
                return response_text
            else:
                print(f"✗ Invalid response format: '{response_text}'. Expected format: 'Action: [details]'.")

        except Exception as e:
            print(f"An error occurred while calling the OpenAI API: {e}")

    print("AI failed to provide a valid action after 3 attempts.")
    return "Action: skip"

def board_to_string(board):
    """
    Converts the board to a clear, readable string format for the AI.
    Shows row/column indices and uses visual symbols.
    """
    result = "Current Gomoku Board (15x15):\n"
    result += "Column:  " + "".join(f"{i:2}" for i in range(15)) + "\n"
    result += "Row:\n"
    
    for i, row in enumerate(board):
        result += f"{i:2}:     "
        for cell in row:
            if cell == 0:
                result += " ."
            elif cell == 1:
                result += " X"
            elif cell == 2:
                result += " O"
        result += "\n"
    
    result += "\nLEGEND:\n"
    result += "  . = EMPTY (you can place here)\n"
    result += "  X = Player 1 pieces\n"
    result += "  O = Player 2 pieces\n"
    result += "\nIMPORTANT: You can ONLY place your piece on positions marked with '.' (dot)\n"
    
    # Add list of available moves for clarity
    available_moves = []
    for i in range(15):
        for j in range(15):
            if board[i][j] == 0:
                available_moves.append(f"({i},{j})")
    
    if len(available_moves) > 0:
        result += f"\nSome available positions: {', '.join(available_moves[:20])}"
        if len(available_moves) > 20:
            result += "... and more"
    
    return result