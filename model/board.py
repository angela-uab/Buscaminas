import random

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [['.' for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()
        self._place_mines()

    def _place_mines(self):
        while len(self.mine_positions) < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            self.mine_positions.add((row, col))

        for row, col in self.mine_positions:
            self.board[row][col] = 'M'
    
    def display_board(self):
        for row in self.board:
            print(' '.join(row))

