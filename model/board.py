from model.tile import Tile
import random


class Board:
    DIFFICULTY_SETTINGS = {
        1: {"size": 6, "bombs": 8},
        2: {"size": 8, "bombs": 16},
        3: {"size": 10, "bombs": 32},
    }

    def __init__(self, difficulty):
        if difficulty not in self.DIFFICULTY_SETTINGS:
            raise ValueError("Please choose 1, 2, or 3.")

        self.size = self.DIFFICULTY_SETTINGS[difficulty]["size"]
        self.total_bombs = self.DIFFICULTY_SETTINGS[difficulty]["bombs"]
        self.is_game_lost = False
        self.tiles = self._initialize_board()

    def _initialize_board(self):
        
        tiles = [[Tile() for _ in range(self.size)] for _ in range(self.size)]
        bomb_positions = random.sample(range(self.size * self.size), self.total_bombs)

        for pos in bomb_positions:
            row, col = divmod(pos, self.size)
            tiles[row][col].is_bomb = True

        return tiles

    def reveal_tile(self, x, y):
        
        tile = self.tiles[x][y]
        tile.reveal()
        if tile.is_bomb:
            self.is_game_lost = True

    def is_game_won(self):
        
        for row in self.tiles:
            for tile in row:
                if not tile.is_bomb and not tile.is_revealed:
                    return False
        return True

