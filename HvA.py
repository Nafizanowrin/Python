# This code creates a simple GUI for the Tic Tac Toe game using Tkinter. Players can click on the buttons to make their
#  moves, and an AI opponent (with random move strategy) is implemented for the 'O' player. The game checks for a win or 
# draw after each move and displays a message box accordingly.
import tkinter as tk
from tkinter import messagebox
import math

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

def on_click(row, col):
    global current_player

    if buttons[row][col]["text"] == "":
        buttons[row][col]["text"] = "X"
        board[row][col] = "X"
        print_board(board)

        winner = check_winner(board)
        if winner:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            reset_game()
            return
        elif is_board_full(board):
            messagebox.showinfo("Game Over", "It's a tie!")
            reset_game()
            return

        row, col = find_best_move(board)
        buttons[row][col]["text"] = "O"
        board[row][col] = "O"
        print_board(board)

        winner = check_winner(board)
        if winner:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            reset_game()
            return
        elif is_board_full(board):
            messagebox.showinfo("Game Over", "It's a tie!")
            reset_game()
            return

def reset_game():
    global current_player, board
    current_player = "X"
    board = [["" for _ in range(3)] for _ in range(3)]

    for row in range(3):
        for col in range(3):
            buttons[row][col]["text"] = ""

# Create the main window
root = tk.Tk()
root.title("Human vs AI Tic-Tac-Toe Gameplay")

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
# def check_win(self, player):
#     for row in self.board:
#         if all(cell == player for cell in row):
#             return True

#     for col in range(3):
#         if all(self.board[row][col] == player for row in range(3)):
#             return True

#     if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2-i] == player for i in range(3)):
#         return True

#     return False

# Initialize game variables
current_player = "X"
board = [["" for _ in range(3)] for _ in range(3)]

print_board(board)

root.mainloop()
