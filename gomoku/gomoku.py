# gomoku.py

import time
from ai_player import get_ai_move, initialize_client_manually

# --- Game Constants ---
BOARD_SIZE = 15
MAX_MOVES_PER_PLAYER = 100

# --- Game State ---
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
PLAYER_MODELS = {
    1: "gpt-4o-mini",
    2: "gpt-4o"
}
player_move_counts = {1: 0, 2: 0}

def print_board(current_player):
    """Prints the Gomoku board to the console."""
    print("\n" * 2)
    print("=============================================")
    player_name = PLAYER_MODELS.get(current_player, "Unknown")
    p1_moves = player_move_counts[1]
    p2_moves = player_move_counts[2]
    print(f"  Player 1 (X): {p1_moves}/{MAX_MOVES_PER_PLAYER} | Player 2 (O): {p2_moves}/{MAX_MOVES_PER_PLAYER}")
    print(f"            Turn: Player {current_player} ({player_name})           ")
    print("=============================================")
    print("   " + " ".join(f"{i:<2}" for i in range(BOARD_SIZE)))
    print("  +" + "---" * BOARD_SIZE + "+")

    for i, row in enumerate(board):
        print(f"{i:<2}|", end=" ")
        for cell in row:
            if cell == 0:
                print(" .", end=" ")
            elif cell == 1:
                print(" X", end=" ")
            elif cell == 2:
                print(" O", end=" ")
        print("|")
    
    print("  +" + "---" * BOARD_SIZE + "+")

def check_win(player, row, col):
    """Checks if the current player has won."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

if __name__ == "__main__":
    print("--- Gomoku AI Battle ---")
    print(f"Player 1: {PLAYER_MODELS[1]} (X)")
    print(f"Player 2: {PLAYER_MODELS[2]} (O)")
    print(f"Move Limit: {MAX_MOVES_PER_PLAYER} moves per player.")
    print("--------------------------")

    if not initialize_client_manually():
        print("Could not start the game due to API key issue.")
        exit()

    current_player = 1
    game_over = False
    
    while not game_over:
        print_board(current_player)
        model_name = PLAYER_MODELS[current_player]
        move = get_ai_move(board, current_player, model_name)

        if move:
            row, col = move
            board[row][col] = current_player
            player_move_counts[current_player] += 1
            
            if check_win(current_player, row, col):
                print_board(current_player)
                player_name = PLAYER_MODELS[current_player]
                print(f"\n*** Player {current_player} ({player_name}) wins! ***\n")
                game_over = True
            elif player_move_counts[current_player] >= MAX_MOVES_PER_PLAYER:
                print_board(current_player)
                print(f"\n*** Draw! Player {current_player} reached the move limit of {MAX_MOVES_PER_PLAYER}. ***\n")
                game_over = True
            elif sum(player_move_counts.values()) == BOARD_SIZE * BOARD_SIZE:
                print_board(current_player)
                print("\n*** It's a draw! The board is full. ***\n")
                game_over = True
            else:
                current_player = 2 if current_player == 1 else 1
                time.sleep(1)
        else:
            print("Error: Failed to get a valid move from the AI after multiple attempts. Ending game.")
            game_over = True