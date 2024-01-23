import random

class Board():
    def __init__(self, difficulty):
        match difficulty:
            case 1:
                self.width = 9
                self.height = 9
                self.bombs = 10
            case 2:
                self.width = 16
                self.height = 16
                self.bombs = 40
            case 3:
                self.width = 30
                self.height = 16
                self.bombs = 99
        self.flags = self.bombs
        self.clicked = False
        
    # generate grid of Cell objects
    def generate_grid(self):
        grid = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell("default", j, i))
            grid.append(row)
        self.grid = grid
    
    # place bombs randomly on the grid
    def place_bombs(self):
        bombs = self.bombs
        while bombs > 0:
            row = random.randint(0, self.height-1)
            col = random.randint(0, self.width-1)
            
            if self.grid[row][col].get_value() != "mine":
                self.grid[row][col].set_value("mine")
                bombs -= 1
  
    # get the number of adjacent mines to a given coordinate
    def get_adjacent_mines(self, col, row):
        adjacent_mines = 0
        
        for i in range(-1, 2): # Loop through the 3x3 grid around the coordinate
            for j in range(-1, 2): # Loop through the 3x3 grid around the coordinate
                if col + i >= 0 and col + i < self.width and row + j >= 0 and row + j < self.height:
                    if self.grid[row + j][col + i].get_value() == "mine":
                        adjacent_mines += 1
        
        return adjacent_mines
    
    # reveal all empty spaces adjacent to a given coordinate
    def reveal_empty(self, col, row):
        cell = self.grid[row][col]
        if cell.get_revealed() or cell.get_value() == "mine" or cell.flagged:
            return None
        else:
            cell.set_revealed(True)
            if self.get_adjacent_mines(col, row) == 0:
                cell.set_value("empty")
                for i in range(-1, 2): # Loop through the 3x3 grid around the coordinate
                    for j in range(-1, 2): # Loop through the 3x3 grid around the coordinate
                        # if i == 0 or j == 0: # Skip the coordinate itself and the diagonals
                        if (col + i >= 0 and col + i < self.width) and (row + j >= 0 and row + j < self.height):
                            self.reveal_empty(col + i, row + j)
            else:
                cell.set_value(self.get_adjacent_mines(col, row))
            return None
    
    # reveal a given coordinate
    def click(self, col, row):
        # TODO: If the first click is not a completely empty spot, move the bombs
        cell = self.grid[row][col]
        if not cell.get_revealed() and not cell.flagged:
            if cell.get_value() == "mine":
                if not self.clicked: # If the first click is a mine, replace the bombs
                    self.replace_bombs(col, row)
                    self.clicked = True
                else:
                    cell.set_revealed(True)
            else:
                self.clicked = True
                self.reveal_empty(col, row)
    
    # replace the bombs if the first click is a bomb          
    def replace_bombs(self, col, row):
        self.generate_grid()
        self.place_bombs()
        self.click(col, row)
        
    # flag a given coordinate
    def flag(self, col, row):
        cell = self.grid[row][col]
        if not cell.get_revealed():
            if cell.flagged:
                cell.flagged = False
                self.flags += 1
            elif self.flags > 0:
                cell.flagged = True
                self.flags -= 1
            
    # check if the user has won
    def check_won(self):
        for i in range(self.height):
            for j in range(self.width):
                if not self.grid[i][j].get_revealed() and self.grid[i][j].get_value() != "mine":
                    return False
        return True
    
    # check if the user has lost
    def check_lose(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j].get_revealed() and self.grid[i][j].get_value() == "mine":
                    return True
        return False
      
    # convert the board to a JSON object
    def to_json(self):
        return {
            'flags': self.flags,
            'grid': [[cell.to_json() for cell in row] for row in self.grid],
            'won': self.check_won(),
            'lost': self.check_lose()
        }

class Cell():
    def __init__(self, value, pos_x, pos_y, revealed=False, flagged=False):
        self.__value = value
        self.__revealed = revealed
        self.flagged = flagged
        
    def set_value(self, value):
        self.__value = value
        
    def get_value(self):
        return self.__value
    
    def set_revealed(self, revealed):
        self.__revealed = revealed
        
    def get_revealed(self):
        return self.__revealed
    
    # convert the cell to a JSON object
    def to_json(self):
        return {
            'value': self.__value,
            'revealed': self.__revealed,
            'flagged': self.flagged
        }