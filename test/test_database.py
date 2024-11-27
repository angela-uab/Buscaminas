import pytest
import os
from model.database_manager import DatabaseManager


@pytest.fixture
def test_db():    
    test_db_file = "test_database.db"
    db = DatabaseManager(test_db_file)
    yield db
    db.close()
    if os.path.exists(test_db_file):
        os.remove(test_db_file)  # Elimina la base de datos temporal al final de la prueba.


def test_invalid_insert_player(test_db):
    with pytest.raises(ValueError):
        test_db.insert_player("", 10)  # Nombre vacío no permitido
    with pytest.raises(ValueError):
        test_db.insert_player(None, 10)  # Nombre None no permitido
    with pytest.raises(ValueError):
        test_db.insert_player("Alice", "invalid_score")  # Puntaje debe ser un número


def test_invalid_get_player_by_id(test_db):
    test_db.insert_player("Alice", 10)  # Insertamos un jugador válido
    with pytest.raises(ValueError):
        test_db.get_player_by_id("invalid_id")  # ID no es un entero


def test_invalid_delete_player(test_db):
    test_db.insert_player("Alice", 10)  # Insertamos un jugador válido
    with pytest.raises(ValueError):
        test_db.delete_player("invalid_id")  # ID no es un entero


def test_insert_two_players(test_db):
    # Insertamos dos jugadores válidos
    result_alice = test_db.insert_player("Alice", 10)
    result_bob = test_db.insert_player("Bob", 25)

    assert result_alice is True
    assert result_bob is True

    players = test_db.get_all_players()
    assert len(players) == 2
    assert players[0][1] == "Alice"
    assert players[0][2] == 10
    assert players[1][1] == "Bob"
    assert players[1][2] == 25


def test_delete_player(test_db):
    test_db.insert_player("Alice", 10)
    test_db.insert_player("Bob", 25)

    result = test_db.delete_player(1)
    assert result is True

    players = test_db.get_all_players()
    assert len(players) == 1
    assert players[0][1] == "Bob"


def test_get_player_by_id(test_db):
    test_db.insert_player("Alice", 10)

    player = test_db.get_player_by_id(1)
    assert player is not None
    assert player[1] == "Alice"
    assert player[2] == 10


def test_update_player_score(test_db):
    test_db.insert_player("Alice", 10)
    result = test_db.update_player_score(1, 50)

    assert result is True
    player = test_db.get_player_by_id(1)
    assert player[2] == 50


def test_get_top_players(test_db):
    test_db.insert_player("Alice", 10)
    test_db.insert_player("Bob", 25)
    test_db.insert_player("Charlie", 15)

    top_players = test_db.get_top_players(2)
    assert len(top_players) == 2
    assert top_players[0][1] == "Bob"  # Mejor puntuación
    assert top_players[1][1] == "Charlie"  # Segunda mejor puntuación
