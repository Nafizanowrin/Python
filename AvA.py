import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.root = tk.Tk()
        self.root.title("AI vs AI Tic-Tac-Toe Gameplay")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text="", font=('Helvetica', 20), width=5, height=2,
                                command=lambda i=i, j=j: self.on_button_click(i, j), bg='lightblue', fg="darkblue")
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)
        self.status_label = tk.Label(self.root, text="Player X's turn", font=('Helvetica', 20))
        self.status_label.grid(row=3, column=0, columnspan=3, sticky="ew")
        self.root.after(1000, self.ai_move)

    def ai_move(self):
        if not self.check_winner() and not self.check_draw():
            best_move = None
            best_score = float('-inf') if self.current_player == "O" else float('inf')

            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = self.current_player
                        score = self.minimax(not (self.current_player == "O"))
                        self.board[i][j] = ""
                        if (self.current_player == "O" and score > best_score) or (self.current_player == "X" and score < best_score):
                            best_score = score
                            best_move = (i, j)

            if best_move:
                self.board[best_move[0]][best_move[1]] = self.current_player
                self.buttons[best_move[0]][best_move[1]].config(text=self.current_player)
                if self.check_winner():
                    self.status_label.config(text=f"Player {self.current_player} wins!")
                    messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                    self.root.quit()
                elif self.check_draw():
                    self.status_label.config(text="It's a draw!")
                    messagebox.showinfo("Game Over", "It's a draw!")
                    self.root.quit()
                else:
                    self.current_player = "O" if self.current_player == "X" else "X"
                    self.status_label.config(text=f"Player {self.current_player}'s turn")
                    self.root.after(1000, self.ai_move)

    def minimax(self, maximizing):
        if self.check_winner():
            return 1 if maximizing else -1 
            print("End State:", stateEval)
            return stateEval
        elif self.check_draw():
            print("End State: draw")
            return 0
        
        if maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.minimax(False)
                        self.board[i][j] = ""
                        best_score = max(score, best_score)
                        print(f"Maximizing: Placing 'O' at ({i}, {j}), Score: {score}")  # Debug print for maximizing
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score = self.minimax(True)
                        self.board[i][j] = ""
                        best_score = min(score, best_score)
                        print(f"Minimizing: Placing 'X' at ({i}, {j}), Score: {score}")  # Debug print for minimizing
            return best_score

    def check_winner(self):
        lines = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)], [(2, 0), (1, 1), (0, 2)]
        ]
        for line in lines:
            if self.board[line[0][0]][line[0][1]] != "" and all(self.board[line[0][0]][line[0][1]] == self.board[pos[0]][pos[1]] for pos in line):
                return True
        return False

    def check_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

if __name__ == "__main__":
    game = TicTacToe()
    game.root.mainloop()
