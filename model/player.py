class Player:
    def __init__(self, player_id, name, score):
        self.set_id(player_id)
        self.set_name(name)
        self.set_score(score)

    def get_id(self):
        return self._id

    def set_id(self, player_id):
        if not isinstance(player_id, int) or player_id < 0:
            raise ValueError("ID must be a non-negative integer.")
        self._id = player_id

    def get_name(self):
        return self._name

    def set_name(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = name.strip()

    def get_score(self):
        return self._score

    def set_score(self, score):
        if not isinstance(score, int) or score < 0:
            raise ValueError("Score must be a non-negative integer.")
        self._score = score
