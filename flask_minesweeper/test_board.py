import pytest
from models import Board

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
    
def test_place_bombs():
    board = Board(1)
    board.generate_grid()
    board.place_bombs()
    bombs = 0
    for row in board.grid:
        for cell in row:
            if cell.get_value() == 'mine':
                bombs += 1
    assert bombs == 10
    assert board.bombs == 10
    assert board.flags == 10
    
    board = Board(2)
    board.generate_grid()
    board.place_bombs()
    bombs = 0
    for row in board.grid:
        for cell in row:
            if cell.get_value() == 'mine':
                bombs += 1
    assert bombs == 40
    assert board.bombs == 40
    assert board.flags == 40
    
def test_get_adjacent_mines():
    board = Board(1)
    board.generate_grid()
    board.grid[2][1].set_value('mine')
    board.grid[2][2].set_value('mine')
    assert board.get_adjacent_mines(0, 0) == 0
    assert board.get_adjacent_mines(0, 1) == 1
    assert board.get_adjacent_mines(0, 2) == 1
    assert board.get_adjacent_mines(1, 1) == 2
    
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
    board.grid[2][1].set_value('mine')
    
    assert board.check_lose() == False
    board.grid[2][1].set_revealed(True)
    assert board.check_lose() == True
    
def test_check_won():
    board = Board(1)
    board.generate_grid()
    board.grid[2][1].set_value('mine')
    board.grid[2][2].set_value('mine')
    assert board.check_won() == False
    
    board.reveal_empty(0, 0)
    assert board.check_won() == False
    
    board.reveal_empty(0, 2)
    assert board.check_won() == True