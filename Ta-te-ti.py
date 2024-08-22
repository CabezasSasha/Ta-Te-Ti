import tkinter as tk
from tkinter import messagebox
import random

class TaTeTi:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Ta-Te-Ti de Nanana Web Studio & marketing")
        self.root.configure(bg='#f5f5f5')  # Fondo de la ventana principal
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.difficulty = 'Hard'
        self.create_widgets()

    def create_widgets(self):
        self.buttons = [[tk.Button(self.root, text='', font=('Arial', 20, 'bold'), width=5, height=3,
                                   command=lambda x=x, y=y: self.make_move(x, y),
                                   bg='#e0e0e0', activebackground='#c0c0c0', relief='raised') for y in range(3)] for x in range(3)]

        for x in range(3):
            for y in range(3):
                self.buttons[x][y].grid(row=x, column=y, padx=10, pady=10)

        self.restart_button = tk.Button(self.root, text='Reiniciar', command=self.restart_game, font=('Arial', 14, 'bold'),
                                        bg='#ff6666', fg='white', relief='raised')
        self.restart_button.grid(row=3, column=0, columnspan=3, sticky='nsew', pady=15)

        self.difficulty_label = tk.Label(self.root, text='Dificultad:', font=('Arial', 14, 'bold'), bg='#f5f5f5')
        self.difficulty_label.grid(row=4, column=0, columnspan=3)

        self.difficulty_var = tk.StringVar(value=self.difficulty)
        self.easy_radio = tk.Radiobutton(self.root, text='Fácil', variable=self.difficulty_var, value='Easy',
                                        command=self.set_difficulty, bg='#f5f5f5', fg='#000000', selectcolor='#cccccc',
                                        font=('Arial', 12, 'bold'))
        self.medium_radio = tk.Radiobutton(self.root, text='Medio', variable=self.difficulty_var, value='Medium',
                                           command=self.set_difficulty, bg='#f5f5f5', fg='#000000', selectcolor='#cccccc',
                                           font=('Arial', 12, 'bold'))
        self.hard_radio = tk.Radiobutton(self.root, text='Difícil', variable=self.difficulty_var, value='Hard',
                                         command=self.set_difficulty, bg='#f5f5f5', fg='#000000', selectcolor='#cccccc',
                                         font=('Arial', 12, 'bold'))

        self.easy_radio.grid(row=5, column=0)
        self.medium_radio.grid(row=5, column=1)
        self.hard_radio.grid(row=5, column=2)

    def set_difficulty(self):
        self.difficulty = self.difficulty_var.get()

    def make_move(self, x, y):
        if self.game_over or self.board[x][y] is not None:
            return

        self.board[x][y] = self.current_player
        self.buttons[x][y].config(text=self.current_player, bg='#ffeb3b' if self.current_player == 'X' else '#4caf50')

        if self.check_win(self.current_player):
            self.show_message(f'{self.current_player} gana!')
            self.game_over = True
        elif all(cell is not None for row in self.board for cell in row):
            self.show_message('Es un empate!')
            self.game_over = True
        else:
            self.current_player = 'O'
            self.root.after(500, self.machine_move)

    def machine_move(self):
        if self.game_over:
            return

        if self.difficulty == 'Easy':
            self.random_move()
        elif self.difficulty == 'Medium':
            self.medium_move()
        else:
            self.best_move()

    def random_move(self):
        empty_cells = [(x, y) for x in range(3) for y in range(3) if self.board[x][y] is None]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.board[x][y] = 'O'
            self.buttons[x][y].config(text='O', bg='#ff5722')
            self.check_game_status()

    def medium_move(self):
        # Intentar ganar en un solo movimiento
        for x in range(3):
            for y in range(3):
                if self.board[x][y] is None:
                    self.board[x][y] = 'O'
                    if self.check_win('O'):
                        self.board[x][y] = 'O'
                        self.buttons[x][y].config(text='O', bg='#ff5722')
                        self.check_game_status()
                        return
                    self.board[x][y] = None

        # Bloquear al oponente si puede ganar en su próximo movimiento
        for x in range(3):
            for y in range(3):
                if self.board[x][y] is None:
                    self.board[x][y] = 'X'
                    if self.check_win('X'):
                        self.board[x][y] = 'O'
                        self.buttons[x][y].config(text='O', bg='#ff5722')
                        self.check_game_status()
                        return
                    self.board[x][y] = None

        # Jugar en el mejor lugar disponible (esquina o centro)
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for corner in corners:
            if self.board[corner[0]][corner[1]] is None:
                self.board[corner[0]][corner[1]] = 'O'
                self.buttons[corner[0]][corner[1]].config(text='O', bg='#ff5722')
                self.check_game_status()
                return

        # Jugar en el centro si está disponible
        if self.board[1][1] is None:
            self.board[1][1] = 'O'
            self.buttons[1][1].config(text='O', bg='#ff5722')
            self.check_game_status()
            return

        # Jugar en un espacio libre
        self.random_move()

    def best_move(self):
        best_score = -float('inf')
        best_move = None

        for x in range(3):
            for y in range(3):
                if self.board[x][y] is None:
                    self.board[x][y] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[x][y] = None
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        if best_move:
            x, y = best_move
            self.board[x][y] = 'O'
            self.buttons[x][y].config(text='O', bg='#ff5722')

        self.check_game_status()

    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner()
        if winner == 'O':
            return 10 - depth
        elif winner == 'X':
            return depth - 10
        elif all(cell is not None for row in board for cell in row):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for x in range(3):
                for y in range(3):
                    if board[x][y] is None:
                        board[x][y] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[x][y] = None
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for x in range(3):
                for y in range(3):
                    if board[x][y] is None:
                        board[x][y] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[x][y] = None
                        best_score = min(score, best_score)
            return best_score

    def check_game_status(self):
        if self.check_win('O'):
            self.show_message('O gana!')
            self.game_over = True
        elif self.check_win('X'):
            self.show_message('X gana!')
            self.game_over = True
        elif all(cell is not None for row in self.board for cell in row):
            self.show_message('Es un empate!')
            self.game_over = True
        else:
            self.current_player = 'X'

    def check_win(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def check_winner(self):
        if self.check_win('O'):
            return 'O'
        elif self.check_win('X'):
            return 'X'
        return None

    def show_message(self, message):
        messagebox.showinfo("Resultado", message)

    def restart_game(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        for row in self.buttons:
            for button in row:
                button.config(text='', bg='#e0e0e0')

if __name__ == "__main__":
    root = tk.Tk()
    game = TaTeTi(root)
    root.mainloop()
