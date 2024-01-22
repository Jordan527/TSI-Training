import pytest
from minesweeper import Board

def test_generate_grid():
    board = Board(1)
    board.generate_grid()
    assert board.width == 9
    assert board.height == 9
    assert board.bombs == 10
    
    board = Board(2)
    board.generate_grid()
    assert board.width == 16
    assert board.height == 16
    assert board.bombs == 40
    
    board = Board(3)
    board.generate_grid()
    assert board.width == 16
    assert board.height == 30
    assert board.bombs == 99
    
def test_get_adjacent_mines():
    board = Board(1)
    board.generate_grid()
    board.grid[2][1].set_value('M')
    board.grid[2][2].set_value('M')
    assert board.get_adjacent_mines(0, 0) == 0
    assert board.get_adjacent_mines(0, 1) == 1
    assert board.get_adjacent_mines(0, 2) == 1
    assert board.get_adjacent_mines(1, 1) == 2
    
def test_reveal_empty():
    board = Board(1)
    board.generate_grid()
    board.grid[2][1].set_value('M')
    board.grid[2][2].set_value('M')
    
    board.reveal_empty(0, 0)
    expected_board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [1, 2, 2, 1, ' ', ' ', ' ', ' ', ' '],
        ['*', '*', '*', 1, ' ', ' ', ' ', ' ', ' '],
        [1, 2, 2, 1, ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]
    
    actual_board = []
    for row in board.grid:
        actual_row = [cell.get_value() if cell.get_revealed() else board.default_value for cell in row]
        actual_board.append(actual_row)
    assert actual_board == expected_board
    
def test_flag():
    board = Board(1)
    board.generate_grid()
    
    board.flag(0, 0)
    assert board.grid[0][0].flagged == True
    assert board.flags == board.bombs - 1
    
    board.flag(0, 0)
    assert board.grid[0][0].flagged == False
    assert board.flags == board.bombs
    
def test_lose():
    board = Board(1)
    board.generate_grid()
    board.grid[2][1].set_value('M')
    
    assert board.check_lose() == False
    board.grid[2][1].set_revealed(True)
    assert board.check_lose() == True
    
def test_click():
    board = Board(1)
    board.generate_grid()
    board.grid[2][1].set_value('M')
    board.grid[2][2].set_value('M')
    
    board.click(0, 0)
    expected_board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [1, 2, 2, 1, ' ', ' ', ' ', ' ', ' '],
        ['*', '*', '*', 1, ' ', ' ', ' ', ' ', ' '],
        [1, 2, 2, 1, ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]
    
    actual_board = []
    for row in board.grid:
        actual_row = [cell.get_value() if cell.get_revealed() else board.default_value for cell in row]
        actual_board.append(actual_row)
    assert actual_board == expected_board
    
    board.flag(1, 2)
    board.click(1, 2)
    assert board.check_lose() == False
    
    board.flag(1, 2)
    board.click(1, 2)
    assert board.check_lose() == True
    
def test_check_won():
    board = Board(1)
    board.generate_grid()
    board.grid[2][1].set_value('M')
    board.grid[2][2].set_value('M')
    assert board.check_won() == False
    
    board.reveal_empty(0, 0)
    assert board.check_won() == False
    
    board.reveal_empty(0, 2)
    assert board.check_won() == True