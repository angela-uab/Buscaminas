import sqlite3

class DatabaseManager:
    def __init__(self, database_name="database.db"):
        """
        Inicializa el gestor de base de datos y conecta con el archivo SQLite.
        """
        # Precondición: database_name debe ser una cadena no vacía.
        if not isinstance(database_name, str) or not database_name.strip():
            raise ValueError("El nombre de la base de datos debe ser una cadena no vacía.")
        
        self.database_name = database_name
        self.connection = self._connect()
        self._initialize_database()

        # Invariante: La conexión con la base de datos debe estar abierta.
        assert self.connection is not None, "La conexión a la base de datos no se pudo establecer."

    def _connect(self):
        """Conecta con la base de datos SQLite."""
        connection = sqlite3.connect(self.database_name)
        # Postcondición: Se debe devolver una conexión válida.
        assert connection is not None, "No se pudo establecer la conexión a la base de datos."
        return connection

    def _initialize_database(self):
        """Crea la tabla `players` si no existe."""
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
        """)
        self.connection.commit()

        # Invariante: La tabla `players` debe existir después de este método.
        cursor = self.connection.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='players'
        """)
        assert cursor.fetchone() is not None, "La tabla 'players' no se creó correctamente."

    def insert_player(self, name, score):
        """Inserta un jugador en la base de datos y devuelve su ID."""
        # Precondiciones
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre debe ser una cadena no vacía.")
        if not isinstance(score, int) or score < 0:
            raise ValueError("El puntaje debe ser un entero no negativo.")

        try:
            cursor = self.connection.execute(
                "INSERT INTO players (name, score) VALUES (?, ?)", (name, score)
            )
            self.connection.commit()

            # Postcondición: El ID del jugador insertado debe ser mayor a 0.
            assert cursor.lastrowid > 0, "El jugador no fue insertado correctamente."
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def get_all_players(self):
        """Devuelve todos los jugadores de la tabla."""
        try:
            cursor = self.connection.execute("SELECT * FROM players")
            players = cursor.fetchall()

            # Postcondición: El resultado debe ser una lista.
            assert isinstance(players, list), "El resultado no es una lista."
            return players
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def get_player_by_id(self, player_id):
        """Devuelve un jugador por su ID."""
        # Precondición: player_id debe ser un entero positivo.
        if not isinstance(player_id, int) or player_id <= 0:
            raise ValueError("El ID del jugador debe ser un entero positivo.")

        try:
            cursor = self.connection.execute("SELECT * FROM players WHERE id = ?", (player_id,))
            player = cursor.fetchone()

            # Postcondición: El resultado puede ser None o una tupla.
            assert player is None or isinstance(player, tuple), "El resultado no es válido."
            return player
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def delete_player(self, player_id):
        """Elimina un jugador por su ID."""
        # Precondición: player_id debe ser un entero positivo.
        if not isinstance(player_id, int) or player_id <= 0:
            raise ValueError("El ID del jugador debe ser un entero positivo.")

        try:
            cursor = self.connection.execute("DELETE FROM players WHERE id = ?", (player_id,))
            self.connection.commit()

            # Postcondición: El número de filas afectadas debe ser 0 o 1.
            assert cursor.rowcount in (0, 1), "Número inesperado de filas eliminadas."
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def update_player_score(self, player_id, new_score):
        """Actualiza el puntaje de un jugador por su ID."""
        # Precondiciones
        if not isinstance(player_id, int) or player_id <= 0:
            raise ValueError("El ID del jugador debe ser un entero positivo.")
        if not isinstance(new_score, int) or new_score < 0:
            raise ValueError("El puntaje debe ser un entero no negativo.")

        try:
            cursor = self.connection.execute(
                "UPDATE players SET score = ? WHERE id = ?", (new_score, player_id)
            )
            self.connection.commit()

            # Postcondición: El número de filas afectadas debe ser 0 o 1.
            assert cursor.rowcount in (0, 1), "Número inesperado de filas actualizadas."
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def get_top_players(self, limit=5):
        """Devuelve los jugadores con los mejores puntajes, limitado a 'limit'."""
        # Precondición: limit debe ser un entero positivo.
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("El límite debe ser un entero positivo.")

        try:
            cursor = self.connection.execute(
                "SELECT * FROM players ORDER BY score DESC LIMIT ?", (limit,)
            )
            players = cursor.fetchall()

            # Postcondición: El resultado debe ser una lista.
            assert isinstance(players, list), "El resultado no es una lista."
            return players
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def close(self):
        """Cierra la conexión con la base de datos."""
        if self.connection:
            self.connection.close()
            self.connection = None  # Asegura que la conexión se invalida tras cerrarla

        # Postcondición: La conexión debe estar cerrada.
        assert self.connection is None, "La conexión no se cerró correctamente."


    def __enter__(self):
        """Habilita el uso de context managers."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Cierra la conexión al salir del contexto."""
        self.close()
