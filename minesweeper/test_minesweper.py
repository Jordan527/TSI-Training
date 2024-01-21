import pytest
from minesweeper import generate_apparent_board, generate_real_board, place_bombs, generate_boards, get_adjacent_mines, reveal_empty, check_win, reveal_mines

def test_generate_apparent_board():
    apparent_board = generate_apparent_board(5, 5)
    assert len(apparent_board) == 5
    assert len(apparent_board[0]) == 5
    for i in range(len(apparent_board)):
        for j in range(len(apparent_board[0])):
            assert apparent_board[i][j] == '*'
            
def test_generate_real_board():
    real_board = generate_real_board(5, 5)
    assert len(real_board) == 5
    assert len(real_board[0]) == 5
    for i in range(len(real_board)):
        for j in range(len(real_board[0])):
            assert real_board[i][j] == ' '
            
def test_place_bombs():
    real_board = generate_real_board(5, 5)
    real_board = place_bombs(real_board, 5)
    assert len(real_board) == 5
    assert len(real_board[0]) == 5
    count = 0
    for i in range(len(real_board)):
        for j in range(len(real_board[0])):
            if real_board[i][j] == 'M':
                count += 1
    assert count == 5

def test_generate_boards():
    apparent_board, real_board, flags = generate_boards(1)
    assert len(apparent_board) == 9
    assert len(apparent_board[0]) == 9
    assert len(real_board) == 9
    assert len(real_board[0]) == 9
    assert flags == 10
    
def test_get_adjacent_mines():
    board = generate_real_board(5, 5)
    board[2][1] = 'M'
    board[2][2] = 'M'
    board = [
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', 'M', 'M', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ']
    ]
    assert get_adjacent_mines(board, 0, 0) == 0
    assert get_adjacent_mines(board, 0, 1) == 1
    assert get_adjacent_mines(board, 0, 2) == 1
    assert get_adjacent_mines(board, 1, 1) == 2
    
def test_reveal_empty():
    apparent_board = generate_apparent_board(5, 5)
    real_board = generate_real_board(5, 5)
    real_board[2][1] = 'M'
    real_board[2][2] = 'M'
    
    apparent_board = reveal_empty(real_board, apparent_board, 0, 0)
    expected_board = [
        [' ', ' ', ' ', ' ', ' '],
        [1, 2, 2, 1, ' '],
        ['*', '*', '*', 1, ' '],
        [1, 2, 2, 1, ' '],
        [' ', ' ', ' ', ' ', ' ']
    ]
    assert apparent_board == expected_board
    
    apparent_board = generate_apparent_board(5, 5)
    real_board[4][4] = 'M'
    apparent_board = reveal_empty(real_board, apparent_board, 0, 0)
    expected_board = [
        [' ', ' ', ' ', ' ', ' '],
        [1, 2, 2, 1, ' '],
        ['*', '*', '*', 1, ' '],
        ['*', '*', '*', '*', 1],
        ['*', '*', '*', '*', '*']
    ]
    assert apparent_board == expected_board
    
def test_check_win():
    apparent_board = generate_apparent_board(5, 5)
    real_board = generate_real_board(5, 5)
    real_board[2][1] = 'M'
    real_board[2][2] = 'M'
    apparent_board = reveal_empty(real_board, apparent_board, 0, 0)
    assert check_win(apparent_board, real_board) == False
    
    apparent_board = reveal_empty(real_board, apparent_board, 0, 2)
    assert check_win(apparent_board, real_board) == True
    
def test_reveal_mines():
    board = generate_apparent_board(5, 5)
    real_board = generate_real_board(5, 5)
    real_board[2][1] = 'M'
    real_board[2][2] = 'M'
    apparent_board = reveal_mines(board, real_board)
    expected_board = [
        ['*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*'],
        ['*', 'M', 'M', '*', '*'],
        ['*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*']
    ]
    assert apparent_board == expected_board

    board = generate_apparent_board(5, 5)
    apparent_board = reveal_empty(real_board, board, 0, 0)
    new_apparent_board = reveal_mines(apparent_board, real_board)
    expected_board = [
        [' ', ' ', ' ', ' ', ' '],
        [1, 2, 2, 1, ' '],
        ['*', 'M', 'M', 1, ' '],
        [1, 2, 2, 1, ' '],
        [' ', ' ', ' ', ' ', ' ']
    ]
    assert new_apparent_board == expected_board
    
    apparent_board[2][0] = 'F'
    new_apparent_board = reveal_mines(apparent_board, real_board)
    expected_board = [
        [' ', ' ', ' ', ' ', ' '],
        [1, 2, 2, 1, ' '],
        ['F', 'M', 'M', 1, ' '],
        [1, 2, 2, 1, ' '],
        [' ', ' ', ' ', ' ', ' ']
    ]
    assert new_apparent_board == expected_board