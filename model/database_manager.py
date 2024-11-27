import sqlite3


class DatabaseManager:
    def __init__(self, database_name="database.db"):
        """
        Inicializa el gestor de base de datos y conecta con el archivo SQLite.
        Si el archivo no existe, se crea automáticamente.
        """
        self.database_name = database_name
        self.connection = self._connect()
        self._initialize_database()

    def _connect(self):
        return sqlite3.connect(self.database_name)

    def _initialize_database(self):
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
        """)
        self.connection.commit()

    def insert_player(self, name, score):
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        if not isinstance(score, int) or score < 0:
            raise ValueError("Score must be a non-negative integer.")

        try:
            self.connection.execute("INSERT INTO players (name, score) VALUES (?, ?)", (name, score))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def get_all_players(self):
        try:
            cursor = self.connection.execute("SELECT * FROM players")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def get_player_by_id(self, player_id):
        if not isinstance(player_id, int):
            raise ValueError("Player ID must be an integer.")
        try:
            cursor = self.connection.execute("SELECT * FROM players WHERE id = ?", (player_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def delete_player(self, player_id):
        if not isinstance(player_id, int):
            raise ValueError("Player ID must be an integer.")

        try:
            self.connection.execute("DELETE FROM players WHERE id = ?", (player_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def update_player_score(self, player_id, new_score):
        if not isinstance(player_id, int):
            raise ValueError("Player ID must be an integer.")
        if not isinstance(new_score, int) or new_score < 0:
            raise ValueError("Score must be a non-negative integer.")

        try:
            self.connection.execute("UPDATE players SET score = ? WHERE id = ?", (new_score, player_id))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def get_top_players(self, limit=5):
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Limit must be a positive integer.")

        try:
            cursor = self.connection.execute("SELECT * FROM players ORDER BY score DESC LIMIT ?", (limit,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def close(self):
        if self.connection:
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()