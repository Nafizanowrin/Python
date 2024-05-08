import tkinter as tk
from tkinter import messagebox, ttk

class TicTacToe:
    def __init__(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg='white')  # Set background color to white
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text="", font=('Helvetica', 20), width=5, height=2,
                                               command=lambda i=i, j=j: self.on_button_click(i, j), bg='lightblue', fg="darkblue")  # Set button background color to pink
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)
        self.status_label = tk.Label(self.root, text="Player X's turn", font=('Helvetica', 20), bg='white')
        self.status_label.grid(row=3, columnspan=3)
        self.game_mode = tk.StringVar()
        self.game_mode.set("Human vs AI")
        self.mode_selector = ttk.Combobox(self.root, textvariable=self.game_mode, values=["Human vs AI", "AI vs AI"], state='readonly')
        self.mode_selector.grid(row=4, columnspan=3)
        self.mode_selector.bind("<<ComboboxSelected>>", self.change_mode)

        self.ai_vs_ai_delay = 1000  # milliseconds

        if self.game_mode.get() == "AI vs AI":
            self.root.after(self.ai_vs_ai_delay, self.ai_move)

    def change_mode(self, event=None):
        self.reset_game()
        if self.game_mode.get() == "AI vs AI":
            self.root.after(self.ai_vs_ai_delay, self.ai_move)

    def on_button_click(self, row, col):
        if self.board[row][col] == "" and not self.check_winner() and not self.check_draw() and self.game_mode.get() == "Human vs AI":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner():
                result_message = f"Player {self.current_player} wins!"
                self.show_result(result_message)
                print(result_message)
            elif self.check_draw():
                result_message = "It's a draw!"
                self.show_result(result_message)
                print(result_message)
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.config(text=f"Player {self.current_player}'s turn")
                if self.current_player == "O":
                    self.ai_move()

    def ai_move(self):
        if not self.check_winner() and not self.check_draw():
            move, best_score = self.find_best_move()
            if move:
                row, col = move
                print(f"AI chose {move} & best score: {best_score}")
                self.board[row][col] = self.current_player
                self.buttons[row][col].config(text=self.current_player)
                if self.check_winner():
                    result_message = f"Player {self.current_player} wins!"
                    self.show_result(result_message)
                    print(result_message)
                elif self.check_draw():
                    result_message = "It's a draw!"
                    self.show_result(result_message)
                    print(result_message)
                else:
                    self.current_player = "O" if self.current_player == "X" else "X"
                    self.status_label.config(text=f"Player {self.current_player}'s turn")
                    if self.game_mode.get() == "AI vs AI":
                        self.root.after(self.ai_vs_ai_delay, self.ai_move)

    def find_best_move(self):
        best_score = float("-inf") if self.current_player == "O" else float("inf")
        best_move = None

        # First move optimization: if the board is empty, pick the center
        if all(self.board[i][j] == "" for i in range(3) for j in range(3)):
            return (1, 1), 0  # Center position

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O" if self.current_player == "O" else "X"
                    score = self.minimax(0, False if self.current_player == "O" else True, float("-inf"), float("inf"))
                    self.board[i][j] = ""
                    if (self.current_player == "O" and score > best_score) or (self.current_player == "X" and score < best_score):
                        best_score = score
                        best_move = (i, j)
        return best_move, best_score

    def minimax(self, depth, is_maximizing, alpha, beta):
        if self.check_winner():
            state_eval = -1 if is_maximizing else 1
            print(f"End State: {state_eval}")
            return state_eval
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
                        score = self.minimax(depth + 1, False, alpha, beta)
                        self.board[i][j] = ""
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        print(f"AI is considering ({i},{j})...")
                        self.board[i][j] = "X"
                        score = self.minimax(depth + 1, True, alpha, beta)
                        self.board[i][j] = ""
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
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
        messagebox.showinfo("Game Over", message)
        self.reset_game()

    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
        self.status_label.config(text="Player X's turn")
        if self.game_mode.get() == "AI vs AI":
            self.root.after(self.ai_vs_ai_delay, self.ai_move)

if __name__ == "__main__":
    game = TicTacToe()
    game.root.mainloop()
