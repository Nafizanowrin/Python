import tkinter as tk
from tkinter import messagebox
import math
import random


def print_board(board):
    print("Current Board State:")
    for row in board:
        print(" | ".join(row))
        print("-" * 5)
    print()

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != "":
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]

    return None

def is_board_full(board):
    for row in board:
        if "" in row:
            return False
    return True

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner:
        return 1 if winner == 'O' else -1 if winner == 'X' else 0

    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ""
                    best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    best_score = -math.inf
    best_move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = "O"
                score = minimax(board, 0, False)
                board[row][col] = ""
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

def ai_move():
    global current_player

    row, col = find_best_move(board)
    buttons[row][col]["text"] = current_player
    board[row][col] = current_player

    print_board(board)  # Print the board state after "X" AI makes its move
   
    winner = check_winner(board)
    if winner:
        print_board(board)
        print(f"Player {winner} wins!")
        messagebox.showinfo("Game Over", f"Player {winner} wins!")
        reset_game()
        return
    elif is_board_full(board):
        print_board(board)
        print("It's a tie!")
        messagebox.showinfo("Game Over", "It's a tie!")
        reset_game()
        return

    current_player = "X" if current_player == "O" else "O"
    root.after(1000, ai_move)  # Schedule next AI move after 1 second

#  With this modification, the "X" player will choose a random available move instead of always reacting to 
# the "O" player's moves. This should make the gameplay more dynamic and less predictable.
def find_best_move(board):
    available_moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                available_moves.append((row, col))
    return random.choice(available_moves) if available_moves else None


def reset_game():
    global current_player, board
    current_player = "X"
    board = [["" for _ in range(3)] for _ in range(3)]

    for row in range(3):
        for col in range(3):
            buttons[row][col]["text"] = ""

# Create the main window
root = tk.Tk()
root.title("AI vs AI Tic-Tac-Toe Gameplay")

# Create the buttons for the game board
buttons = []
for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(root, text="", font=("Helvetica", 20), width=5, height=2,
                   command=lambda row=i, col=j: on_click(row, col),
                   bg="lightblue", fg="darkblue")
        button.grid(row=i, column=j, padx=5, pady=5)
        row_buttons.append(button)
    buttons.append(row_buttons)


# Checking Win Condition:
# def check_win(self, player): Defines a method to check if the specified player has won the game.
# def check_win(player, board):
#     # Check rows
#     for row in board:
#         if all(cell == player for cell in row):
#             return True

#     # Check columns
#     for col in range(3):
#         if all(board[row][col] == player for row in range(3)):
#             return True

#     # Check diagonals
#     if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
#         return True

#     return False



# Initialize game variables
current_player = "X"
board = [["" for _ in range(3)] for _ in range(3)]

print_board(board)

# Perform AI moves
ai_move()

root.mainloop()


