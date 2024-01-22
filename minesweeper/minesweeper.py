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
                self.width = 16
                self.height = 30
                self.bombs = 99
        self.flags = self.bombs
        self.values = (self.width * self.height) - self.bombs
        self.empty_value = " "
        self.default_value = "*"
        self.mine_value = "M"
        self.flag_value = "F"
        
    # generate grid of Cell objects
    def generate_grid(self):
        grid = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell(self.default_value, j, i))
            grid.append(row)
        self.grid = grid
    
    # place bombs randomly on the grid
    def place_bombs(self):
        bombs = self.bombs
        while bombs > 0:
            row = random.randint(0, self.height-1)
            col = random.randint(0, self.width-1)
            
            if self.grid[row][col].get_value() != self.mine_value:
                self.grid[row][col].set_value(self.mine_value)
                bombs -= 1
         
    # print the instructions to the user
    def print_instructions(self, invalid_format=False):
        print()
        if invalid_format:
            print("Please format your action according the instructions below:")
        print("1. To select a coordinate, enter the row and column (example: 2 3)")
        print("2. To flag or unflag a coordinate, enter the row and column, followed by 'F' (example: 2 3 F)")
        print("3. To view these instructions again, enter 'help'")
        print("4. To restart the game, enter 'restart'")
        print("5. To quit, enter 'quit'")
                
    # display the board to the user
    def display_board(self, show_mines=False):
        print()
        top_nums = "   "
        if self.width >= 10:
            top_nums += " "
        for i in range(self.width):
            top_nums += f" {i+1} "
            if i + 1 < 10:
                top_nums += " "
        print(top_nums)
        for i in range(self.height):
            row = self.grid[i]
            output = f"{i+1} "
            if self.height >= 10 and i + 1 < 10:
                output += " "
            output += "|"
            for cell in row:
                if (cell.get_revealed() and not cell.flagged) or show_mines:
                    output += f" {cell.get_value()} |"
                elif cell.flagged:
                    output += f" {self.flag_value} |"
                else:
                    output += f" {self.default_value} |"
            print(output)
       
    # get the users action
    def get_user_action(self):
        while True:
            action = input("\nAction: ").strip()
            try:
                if action.lower() == 'help':
                    self.print_instructions()
                elif action.lower() == 'restart':
                    print()
                    minesweeper()
                    return None, None, None
                elif action.lower() == 'quit':
                    print("\nThanks for playing!")
                    exit()
                else:
                    valid = True
                    split = action.split(" ")
                    split = [x for x in split if x != '']
                    row = int(split[0].strip())
                    col = int(split[1].strip())

                    if valid and (row < 1 or row > self.height):
                        print(f'Please enter a row value between 1 and {self.height}')
                        valid = False
                    
                    if col < 1 or col > self.width:
                        print(f'Please enter a column value between 1 and {self.width}')
                        valid = False

                    if valid and len(split) > 2:
                        if split[2].strip().lower() == "f":
                            flag = True
                        else:
                            self.print_instructions(True)
                            valid = False
                    else:
                        flag = False
                            
                    if valid:
                        return col-1, row-1, flag
            except Exception as e:
                self.print_instructions(True)
       
    # get the number of adjacent mines to a given coordinate
    def get_adjacent_mines(self, col, row):
        adjacent_mines = 0
        
        for i in range(-1, 2): # Loop through the 3x3 grid around the coordinate
            for j in range(-1, 2): # Loop through the 3x3 grid around the coordinate
                if col + i >= 0 and col + i < self.width and row + j >= 0 and row + j < self.height:
                    if self.grid[row + j][col + i].get_value() == "M":
                        adjacent_mines += 1
        
        return adjacent_mines
    
    # reveal all empty spaces adjacent to a given coordinate
    def reveal_empty(self, col, row):
        cell = self.grid[row][col]
        if cell.get_revealed() or cell.get_value() == self.mine_value or cell.flagged:
            return None
        else:
            cell.set_revealed(True)
            if self.get_adjacent_mines(col, row) == 0:
                cell.set_value(self.empty_value)
                for i in range(-1, 2): # Loop through the 3x3 grid around the coordinate
                    for j in range(-1, 2): # Loop through the 3x3 grid around the coordinate
                        if i == 0 or j == 0: # Skip the coordinate itself and the diagonals
                            if (col + i >= 0 and col + i < self.width) and (row + j >= 0 and row + j < self.height):
                                self.reveal_empty(col + i, row + j)
            else:
                cell.set_value(self.get_adjacent_mines(col, row))
            return None
    
    # reveal a given coordinate
    def click(self, col, row):
        cell = self.grid[row][col]
        if cell.get_revealed():
            print("This coordinate has already been revealed!")
        elif cell.flagged:
            print("This coordinate is flagged!")
        else:
            if cell.get_value() == self.mine_value:
                cell.set_revealed(True)
            else:
                self.reveal_empty(col, row)
                  
    # flag a given coordinate
    def flag(self, col, row):
        if self.grid[row][col].get_revealed():
            print("This coordinate has already been revealed!")
        elif self.grid[row][col].flagged:
            self.grid[row][col].flagged = False
            self.flags += 1
        else:
            self.grid[row][col].flagged = True
            self.flags -= 1
            
    # check if the user has won
    def check_won(self):
        for i in range(self.height):
            for j in range(self.width):
                if not self.grid[i][j].get_revealed() and self.grid[i][j].get_value() != self.mine_value:
                    return False
        return True
    
    # check if the user has lost
    def check_lose(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j].get_revealed() and self.grid[i][j].get_value() == self.mine_value:
                    return True
        return False
      
    # run the game
    def run(self):
        self.generate_grid()
        self.place_bombs()
        self.print_instructions()
        while not self.check_won() and not self.check_lose():
            print(f"\nFlags left: {self.flags}")
            self.display_board(True)
            self.display_board()
            col, row, flag = self.get_user_action()
            if col == None:
                break
            if flag:
                self.flag(col, row)
            else:
                self.click(col, row)
                    
        if self.check_lose():
            print("You hit a mine!")
            self.display_board(True)
        elif self.check_won():
            print("You win!")
            self.display_board(True)
    

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

# Get the users choice of difficulty
def get_difficulty():    
    print("What difficulty would you like to play? \n1. Beginner \n2. Intermediate \n3. Advanced\n")
    difficulty = input("Choice: ").strip()
    
    while True:
        try:
            match int(difficulty):
                case 1 | 2 | 3:
                    return int(difficulty)
                case _:
                    difficulty = input("Please choose either 1, 2 or 3: ").strip()
        except Exception as e:
            difficulty = input("Please enter a number: ").strip()
        
def minesweeper():
    difficulty = get_difficulty()
    board = Board(difficulty)
    board.run()

if __name__ == "__main__":    
    minesweeper()