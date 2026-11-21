def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def display_board(board):
    print("\n")
    for i, row in enumerate(board):
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if i < 2:
            print("---+---+---")
    print("\n")

def display_positions():
    print("\nPositions:")
    print(" 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 \n")

def check_win(board, symbol):
    # Rows
    for row in board:
        if row[0] == row[1] == row[2] == symbol:
            return True
    # Columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == symbol:
            return True
    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] == symbol:
        return True
    if board[0][2] == board[1][1] == board[2][0] == symbol:
        return True
    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def get_valid_move(board, player_name, symbol):
    while True:
        try:
            move_input = input(f"{player_name} ({symbol}) - Enter position (1-9): ").strip()
            if not move_input:
                print(" Input cannot be empty!")
                continue
            if not move_input.isdigit():
                print(" Please enter number 1-9 only.")
                continue
            pos = int(move_input)
            if pos < 1 or pos > 9:
                print(" Out of range! 1-9 only.")
                continue
            row = (pos - 1) // 3
            col = (pos - 1) % 3
            if board[row][col] != " ":
                print(" Cell already occupied!")
                continue
            return row, col
        except Exception as e:
            print(f" Error: {e}. Try again.")

def main():
    print("="*40)
    print("  TIC-TAC-TOE GAME")
    print("="*40)
    
    p1_name = input("Enter Player 1 name (X): ").strip() or "Player 1"
    p2_name = input("Enter Player 2 name (O): ").strip() or "Player 2"
    scores = {p1_name: 0, p2_name: 0, "Draws": 0}
    
    display_positions()
    
    while True:
        board = create_board()
        current_player, current_symbol = p1_name, "X"
        
        while True:
            display_board(board)
            print(f"Turn: {current_player} ({current_symbol})")
            row, col = get_valid_move(board, current_player, current_symbol)
            board[row][col] = current_symbol
            
            if check_win(board, current_symbol):
                display_board(board)
                print(f"🎉 {current_player} WINS!")
                scores[current_player] += 1
                break
            if check_draw(board):
                display_board(board)
                print("🤝 Draw!")
                scores["Draws"] += 1
                break
            if current_symbol == "X":
                current_player, current_symbol = p2_name, "O"
            else:
                current_player, current_symbol = p1_name, "X"
        
        print(f"\nScore - {p1_name}: {scores[p1_name]} | {p2_name}: {scores[p2_name]} | Draws: {scores['Draws']}")
        
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again not in ["y", "yes"]:
            print("Thanks for playing! Bye! 👋")
            break

if __name__ == "__main__":
    main()