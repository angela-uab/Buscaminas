class Tile:
    def __init__(self):
        self._is_bomb = False
        self._is_revealed = False
        self._neighboring_bombs = 0

    @property
    def is_bomb(self):
        return self._is_bomb

    @is_bomb.setter
    def is_bomb(self, value):
        self._is_bomb = value

    @property
    def is_revealed(self):
        return self._is_revealed

    def reveal(self):
        self._is_revealed = True

    @property
    def neighboring_bombs(self):
        return self._neighboring_bombs

    @neighboring_bombs.setter
    def neighboring_bombs(self, value):
        self._neighboring_bombs = value

    def display(self):
        if self.is_revealed:
            return "X" if self.is_bomb else str(self.neighboring_bombs)
        return " "
