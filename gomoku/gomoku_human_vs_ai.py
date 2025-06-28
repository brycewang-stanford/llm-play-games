import time
from ai_player import get_ai_move, initialize_client_manually

BOARD_SIZE = 15
MAX_MOVES_PER_PLAYER = 100

board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
player_move_counts = {1: 0, 2: 0}
PLAYER_MODELS = {2: "gpt-4o"}  # AI 作为玩家2

def print_board():
    print("\n" * 2)
    print("=============================================")
    p1_moves = player_move_counts[1]
    p2_moves = player_move_counts[2]
    print(f"  你 (X): {p1_moves}/{MAX_MOVES_PER_PLAYER} | AI (O): {p2_moves}/{MAX_MOVES_PER_PLAYER}")
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

def get_human_move():
    while True:
        try:
            move = input("请输入你的落子坐标 (格式: 行,列，例如 7,8): ")
            row, col = map(int, move.strip().split(","))
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                if board[row][col] == 0:
                    return row, col
                else:
                    print("该位置已被占用，请重新输入。")
            else:
                print("坐标超出范围，请输入 0-14 之间的数字。")
        except Exception:
            print("输入格式错误，请输入如 7,8 这样的格式。")

if __name__ == "__main__":
    print("--- Gomoku 人机对战 ---")
    print("你是 Player 1 (X)，AI 是 Player 2 (O)")
    print(f"每人最多 {MAX_MOVES_PER_PLAYER} 步。输入格式如 7,8")
    print("--------------------------")

    if not initialize_client_manually():
        print("无法初始化 OpenAI 客户端，游戏无法开始。")
        exit()

    current_player = 1
    game_over = False

    while not game_over:
        print_board()
        if current_player == 1:
            row, col = get_human_move()
        else:
            print("AI 正在思考...")
            move = get_ai_move(board, 2, PLAYER_MODELS[2])
            if move:
                row, col = move
                print(f"AI 落子: {row},{col}")
            else:
                print("AI 未能给出有效落子，游戏结束。")
                break
        board[row][col] = current_player
        player_move_counts[current_player] += 1
        if check_win(current_player, row, col):
            print_board()
            if current_player == 1:
                print("\n*** 恭喜你获胜！***\n")
            else:
                print("\n*** AI 获胜！***\n")
            game_over = True
        elif player_move_counts[current_player] >= MAX_MOVES_PER_PLAYER:
            print_board()
            print(f"\n*** 平局！Player {current_player} 达到步数上限。***\n")
            game_over = True
        elif sum(player_move_counts.values()) == BOARD_SIZE * BOARD_SIZE:
            print_board()
            print("\n*** 平局！棋盘已满。***\n")
            game_over = True
        else:
            current_player = 2 if current_player == 1 else 1
            if current_player == 2:
                time.sleep(1) 