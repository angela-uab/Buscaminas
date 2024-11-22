from model.board import Board

class GameController:
    def __init__(self, rows, cols, mines):
        self.board = Board(rows, cols, mines)

    def play(self):
        print("Bienvenido al Buscaminas de Angela y Muniba!")
        self.board.display_board()
        
