from model.board import Board

def test_create_empty_board():
    rows, cols, mines = 5, 5, 0
    board = Board(rows, cols, mines)

    # Verifica que el tablero tiene las dimensiones correctas
    assert len(board.board) == rows
    assert len(board.board[0]) == cols

    # Verifica que no hay minas en el tablero
    for row in board.board:
        assert all(cell == '.' for cell in row)

def test_place_mines():
    rows, cols, mines = 5, 5, 5
    board = Board(rows, cols, mines)

    # Verifica que hay exactamente 5 minas
    mine_count = sum(row.count('M') for row in board.board)
    assert mine_count == mines


def test_display_board(capsys):
    rows, cols, mines = 5, 5, 0
    board = Board(rows, cols, mines)
    board.display_board()

    captured = capsys.readouterr()
    output = captured.out.strip().split("\n")
    
    # Verifica que cada línea del tablero tiene el número correcto de columnas
    assert len(output) == rows
    assert all(len(line.split()) == cols for line in output)

