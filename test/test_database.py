import pytest
from model.database_manager import DatabaseManager


@pytest.fixture
def test_db():
    """Crea una base de datos para pruebas y limpia los datos antes de cada test."""
    test_db_file = "test_database.db"
    db = DatabaseManager(test_db_file)
    
    # Limpia la tabla antes de cada test
    db.connection.execute("DELETE FROM players")
    db.connection.commit()
    
    yield db
    db.close()  # Cierra la conexión, pero no elimina el archivo

# Partición Equivalente: Verifica entradas inválidas para insertar un jugador.
def test_invalid_insert_player(test_db):
    with pytest.raises(ValueError):
        test_db.insert_player("", 10)  # Nombre vacío no permitido
    with pytest.raises(ValueError):
        test_db.insert_player(None, 10)  # Nombre None no permitido
    with pytest.raises(ValueError):
        test_db.insert_player("Alice", "invalid_score")  # Puntaje debe ser un número

# Statement Coverage: Verifica manejo de errores al buscar un jugador con ID inválido.
def test_invalid_get_player_by_id(test_db):
    player_id = test_db.insert_player("Alice", 10)  # Insertamos un jugador válido
    assert player_id is not None, "El jugador no fue insertado correctamente."
    
    with pytest.raises(ValueError):
        test_db.get_player_by_id("invalid_id")  # ID no es un entero

# Statement Coverage: Verifica manejo de errores al eliminar un jugador con ID inválido.
def test_invalid_delete_player(test_db):
    player_id = test_db.insert_player("Alice", 10)  # Insertamos un jugador válido
    assert player_id is not None, "El jugador no fue insertado correctamente."
    
    with pytest.raises(ValueError):
        test_db.delete_player("invalid_id")  # ID no es un entero

 # Path Coverage: Verifica la inserción de múltiples jugadores y su recuperación.
def test_insert_two_players(test_db):
    # Insertamos dos jugadores válidos
    result_alice = test_db.insert_player("Alice", 10)
    result_bob = test_db.insert_player("Bob", 25)

    assert result_alice is not None, "El jugador 'Alice' no fue insertado correctamente."
    assert result_bob is not None, "El jugador 'Bob' no fue insertado correctamente."

    players = test_db.get_all_players()
    assert len(players) == 2
    assert players[0][1] == "Alice"
    assert players[0][2] == 10
    assert players[1][1] == "Bob"
    assert players[1][2] == 25

# Path Coverage: Verifica el flujo de inserción y eliminación de jugadores.
def test_delete_player(test_db):
    player_id_alice = test_db.insert_player("Alice", 10)
    player_id_bob = test_db.insert_player("Bob", 25)

    assert player_id_alice is not None, "El jugador 'Alice' no fue insertado correctamente."
    assert player_id_bob is not None, "El jugador 'Bob' no fue insertado correctamente."

    result = test_db.delete_player(player_id_alice)
    assert result is True, "El jugador 'Alice' no fue eliminado correctamente."

    players = test_db.get_all_players()
    assert len(players) == 1
    assert players[0][1] == "Bob"

# Decision Coverage: Verifica búsqueda correcta de un jugador por ID.
def test_get_player_by_id(test_db):
    player_id = test_db.insert_player("Alice", 10)
    assert player_id is not None, "El jugador no fue insertado correctamente."

    player = test_db.get_player_by_id(player_id)
    assert player is not None, f"No se encontró el jugador con ID {player_id}."
    assert player[1] == "Alice"
    assert player[2] == 10

# Path Coverage: Verifica la actualización de puntaje para un jugador existente.
def test_update_player_score(test_db):
    player_id = test_db.insert_player("Alice", 10)
    assert player_id is not None, "El jugador no fue insertado correctamente."

    result = test_db.update_player_score(player_id, 50)
    assert result is True, f"No se pudo actualizar el puntaje del jugador con ID {player_id}."

    player = test_db.get_player_by_id(player_id)
    assert player is not None, f"No se encontró el jugador con ID {player_id} tras actualizar la puntuación."
    assert player[2] == 50

# Partición Equivalente y Loop Testing: Verifica recuperación de los mejores puntajes.
def test_get_top_players(test_db):
    player_id_alice = test_db.insert_player("Alice", 10)
    player_id_bob = test_db.insert_player("Bob", 25)
    player_id_charlie = test_db.insert_player("Charlie", 15)

    assert player_id_alice is not None, "El jugador 'Alice' no fue insertado correctamente."
    assert player_id_bob is not None, "El jugador 'Bob' no fue insertado correctamente."
    assert player_id_charlie is not None, "El jugador 'Charlie' no fue insertado correctamente."

    top_players = test_db.get_top_players(2)
    assert len(top_players) == 2
    assert top_players[0][1] == "Bob"  # Mejor puntuación
    assert top_players[1][1] == "Charlie"  # Segunda mejor puntuación

def test_get_top_players_limit_cases(test_db):
    # Límite inferior válido (1 jugador)
    test_db.insert_player("Alice", 50)
    test_db.insert_player("Bob", 100)

    top_players = test_db.get_top_players(1)
    assert len(top_players) == 1
    assert top_players[0][1] == "Bob"  # Mejor puntaje

    # Límite superior (más jugadores que los disponibles)
    top_players = test_db.get_top_players(10)
    assert len(top_players) == 2
    assert top_players[0][1] == "Bob"
    assert top_players[1][1] == "Alice"


