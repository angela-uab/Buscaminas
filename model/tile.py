class Tile:
    def __init__(self):
        self.is_bomb = False
        self.is_revealed = False
        self.neighboring_bombs = 0

    def reveal(self):
        self.is_revealed = True

    def display(self):
        if self.is_revealed:
            return "X" if self.is_bomb else str(self.neighboring_bombs)
        return " "
