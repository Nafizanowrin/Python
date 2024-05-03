# This code creates a simple GUI for the Tic Tac Toe game using Tkinter. Players can click on the buttons to make their
#  moves, and an AI opponent (with random move strategy) is implemented for the 'O' player. The game checks for a win or 
# draw after each move and displays a message box accordingly.
import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.root = tk.Tk()
        self.root.title("HUMAN vs AI Tic-Tac-Toe Gameplay")
        self.root.configure(bg='white')  # Set background color to white
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text="", font=('Helvetica', 20), width=5, height=2,
                                                command=lambda i=i, j=j: self.on_button_click(i, j), bg='lightblue', fg="darkblue")  # Set button background color to pink
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)
        self.status_label = tk.Label(self.root, text="Player X's turn", font=('Helvetica', 20), bg='white')
        self.status_label.grid(row=3, columnspan=3)

    def on_button_click(self, row, col):
        if self.board[row][col] == "" and not self.check_winner() and not self.check_draw():
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner():
                self.show_result(f"Player {self.current_player} wins!")
            elif self.check_draw():
                self.show_result("It's a draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.config(text=f"Player {self.current_player}'s turn")
                if self.current_player == "O":
                    self.ai_move()

    def ai_move(self):
        best_score = float("-inf")
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        row, col = move
        print("AI chose ", move, "& best score:", best_score)
        self.board[row][col] = "O"
        self.buttons[row][col].config(text="O")
        if self.check_winner():
            self.show_result("AI wins!")
        elif self.check_draw():
            self.show_result("It's a draw!")
        else:
            self.current_player = "X"
            self.status_label.config(text="Player X's turn")

    def minimax(self, is_maximizing):
        if self.check_winner():
            stateEval = -1 if is_maximizing else 1 
            print("End State:", stateEval)
            return stateEval
        elif self.check_draw():
            print("End State: draw")
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        print(f"Opponent may choose ({i},{j})")
                        self.board[i][j] = "O"
                        score = self.minimax(False)
                        self.board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        print(f"AI is considering ({i},{j})...")
                        self.board[i][j] = "X"
                        score = self.minimax(True)
                        self.board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score



    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != "":
                return True
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return True
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True

    def show_result(self, message):
        print(message)
        messagebox.showinfo("Game Over", message)
        self.root.quit()

if __name__ == "__main__":
    game = TicTacToe()
    game.root.mainloop()
