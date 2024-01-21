import random

# Generate the apparent board of a given width and height, with the default value in each cell
def generate_apparent_board(width, height):
    global DEFAULT_VALUE
    return [[DEFAULT_VALUE for x in range(width)] for y in range(height)]

# Generate the real board of a given width and height, with the empty value in each cell
def generate_real_board(width, height):
    global EMPTY_VALUE
    return [[EMPTY_VALUE for x in range(width)] for y in range(height)]

# Place a given number of mines randomly on a given board
def place_bombs(board, bombs):
    global MINE_VALUE
    max_col = len(board[0]) - 1
    max_row = len(board) - 1
    
    while bombs > 0:
        row = random.randint(0, max_row)
        col = random.randint(0, max_col)
        
        if board[row][col] != MINE_VALUE:
            board[row][col] = MINE_VALUE
            bombs -= 1
            
    return board
    
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

# Generate the apparent and real boards, and the number of mines
def generate_boards():
    match get_difficulty():
        case 1:
            apparent_board = generate_apparent_board(9, 9)
            real_board = generate_real_board(9, 9)
            real_board = place_bombs(real_board, 10)
            return apparent_board, real_board, 10
        case 2:
            apparent_board = generate_apparent_board(16, 16)
            real_board = generate_real_board(16, 16)
            real_board = place_bombs(real_board, 40)
            return apparent_board, real_board, 40
        case 3:
            apparent_board = generate_apparent_board(16, 30)
            real_board = generate_real_board(16, 30)
            real_board = place_bombs(real_board, 99)
            return apparent_board, real_board, 99

# Print the instructions to the user 
def print_instructions(invalid_format=False):
    global FLAG_VALUE
    if invalid_format:
        print("\nPlease format your action according the instructions below:")
    print("1. To select a coordinate, enter the row and column (example: 2 3)")
    print(f"2. To flag a coordinate, enter the row and column, followed by '{FLAG_VALUE}' (example: 2 3 {FLAG_VALUE})")

# Display the board to the user
def display_board(board):
    print()
    top_nums = "   "
    if len(board) >= 10:
        top_nums += " "
    for i in range(len(board[0])):
        top_nums += f" {i+1} "
        if i + 1 < 10:
            top_nums += " "
    print(top_nums)
    for i in range(len(board)):
        row = board[i]
        output = f"{i+1} "
        if len(board) >= 10 and i + 1 < 10:
            output += " "
        output += "|"
        for value in row:
            output += f" {value} |"
        print(output)

# Get the users action
def get_user_action(max_col, max_row):
    global FLAG_VALUE
    while True:
        action = input("\nAction: ").strip()
        try:
            if action.lower() == 'help':
                print_instructions()
            else:
                valid = True
                
                parts = action.split(" ")
                row = int(parts[0].strip())
                col = int(parts[1].strip())

                if valid and (row < 1 or row > max_row):
                    print(f'Please enter a row value between 1 and {max_row}')
                    valid = False
                
                if col < 1 or col > max_col:
                    print(f'Please enter a column value between 1 and {max_col}')
                    valid = False

                
                if valid and len(parts) > 2:
                    if parts[2].strip().lower() == FLAG_VALUE.lower():
                        flag = True
                    else:
                        print_instructions(True)
                        valid = False
                else:
                    flag = False
                        
                if valid:
                    return col-1, row-1, flag
        except Exception as e:
            print_instructions(True)

# Get the number of adjacent mines to a given coordinate
def get_adjacent_mines(board, col, row):
    global MINE_VALUE
    
    adjacent_mines = 0
    
    for i in range(-1, 2): # Loop through the 3x3 grid around the coordinate
        for j in range(-1, 2): # Loop through the 3x3 grid around the coordinate
            if col + i >= 0 and col + i < len(board[0]) and row + j >= 0 and row + j < len(board): # Check if the coordinate is within the bounds of the board
                if board[row + j][col + i] == MINE_VALUE: # Check if the coordinate is a mine
                    adjacent_mines += 1
    
    return adjacent_mines

# Get the number of adjacent empty spaces to a given coordinate
def get_adjacent_empty(board, col, row):
    global EMPTY_VALUE
    
    adjacent_empty = 0
    
    for i in range(-1, 2): # Loop through the 3x3 grid around the coordinate
        for j in range(-1, 2): # Loop through the 3x3 grid around the coordinate
            if col + i >= 0 and col + i < len(board[0]) and row + j >= 0 and row + j < len(board): # Check if the coordinate is within the bounds of the board
                if board[row + j][col + i] == EMPTY_VALUE: # Check if the coordinate is a mine
                    adjacent_empty += 1
    
    return adjacent_empty

def reveal_empty(board, apparent_board, col, row):
    global DEFAULT_VALUE
    global EMPTY_VALUE
    global FLAG_VALUE
    
    if apparent_board[row][col] == FLAG_VALUE:
        return apparent_board
    
    if apparent_board[row][col] == DEFAULT_VALUE or apparent_board[row][col] == EMPTY_VALUE:
        mines = get_adjacent_mines(board, col, row)
        if mines == 0:
            apparent_board[row][col] = EMPTY_VALUE
        else:
            apparent_board[row][col] = mines
            return apparent_board

        for i in range(-1, 2): # Loop through the 3x3 grid around the coordinate
            for j in range(-1, 2): # Loop through the 3x3 grid around the coordinate
                if i == 0 or j == 0: # Skip the coordinate itself and the diagonals
                    if col + i >= 0 and col + i < len(board[0]) and row + j >= 0 and row + j < len(board): # Check if the coordinate is within the bounds of the board
                        if apparent_board[row + j][col + i] == DEFAULT_VALUE and board[row + j][col + i] == EMPTY_VALUE: # Check if the coordinate is a mine
                            apparent_board = reveal_empty(board, apparent_board, col + i, row + j)

    
    return apparent_board
    

# Run the game
def minesweeper():
    apparent_board, real_board, mines = generate_boards()
    print()
    print_instructions()
    
    max_col = len(real_board[0])
    max_row = len(real_board)
    
    mine_hit = False
    
    while not mine_hit:
        display_board(real_board)
        display_board(apparent_board)
        col, row, flag = get_user_action(max_col, max_row)
        
        if type(apparent_board[row][col]) == int:
            print("This coordinate has already been revealed!")
        else:
            if real_board[row][col] == MINE_VALUE:
                print("You lose!")
                mine_hit = True
            else:
                apparent_board[row][col] = EMPTY_VALUE
                apparent_board = reveal_empty(real_board, apparent_board, col, row)
    
        

if __name__ == "__main__":
    DEFAULT_VALUE = "X"
    MINE_VALUE = "M"
    EMPTY_VALUE = " "
    FLAG_VALUE = "F"
    
    minesweeper()