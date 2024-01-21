import random

# Generate the apparent board of a given width and height, with the default value in each cell
def generate_apparent_board(width, height):
    return [["*" for x in range(width)] for y in range(height)]

# Generate the real board of a given width and height, with the empty value in each cell
def generate_real_board(width, height):
    return [[" " for x in range(width)] for y in range(height)]

# Place a given number of mines randomly on a given board
def place_bombs(board, bombs):
    max_col = len(board[0]) - 1
    max_row = len(board) - 1
    
    while bombs > 0:
        row = random.randint(0, max_row)
        col = random.randint(0, max_col)
        
        if board[row][col] != "M":
            board[row][col] = "M"
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
def generate_boards(difficulty):
    match difficulty:
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
    if invalid_format:
        print("\nPlease format your action according the instructions below:")
    print("1. To select a coordinate, enter the row and column (example: 2 3)")
    print(f"2. To flag or unflag a coordinate, enter the row and column, followed by '{"F"}' (example: 2 3 {"F"})")
    print("3. To view these instructions again, enter 'help'")
    print("4. To restart the game, enter 'restart'")
    print("5. To quit, enter 'quit'")

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
    while True:
        action = input("\nAction: ").strip()
        try:
            if action.lower() == 'help':
                print_instructions()
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

                if valid and (row < 1 or row > max_row):
                    print(f'Please enter a row value between 1 and {max_row}')
                    valid = False
                
                if col < 1 or col > max_col:
                    print(f'Please enter a column value between 1 and {max_col}')
                    valid = False

                if valid and len(split) > 2:
                    if split[2].strip().lower() == "F".lower():
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
    adjacent_mines = 0
    
    for i in range(-1, 2): # Loop through the 3x3 grid around the coordinate
        for j in range(-1, 2): # Loop through the 3x3 grid around the coordinate
            if col + i >= 0 and col + i < len(board[0]) and row + j >= 0 and row + j < len(board): # Check if the coordinate is within the bounds of the board
                if board[row + j][col + i] == "M": # Check if the coordinate is a mine
                    adjacent_mines += 1
    
    return adjacent_mines

# Reveal all empty spaces adjacent to a given coordinate
def reveal_empty(board, apparent_board, col, row):
    if apparent_board[row][col] == "F":
        return apparent_board
    
    if apparent_board[row][col] == "*" or apparent_board[row][col] == " ":
        mines = get_adjacent_mines(board, col, row)
        if mines == 0:
            apparent_board[row][col] = " "
        else:
            apparent_board[row][col] = mines
            return apparent_board

        for i in range(-1, 2): # Loop through the 3x3 grid around the coordinate
            for j in range(-1, 2): # Loop through the 3x3 grid around the coordinate
                if i == 0 or j == 0: # Skip the coordinate itself and the diagonals
                    if col + i >= 0 and col + i < len(board[0]) and row + j >= 0 and row + j < len(board): # Check if the coordinate is within the bounds of the board
                        if apparent_board[row + j][col + i] == "*" and board[row + j][col + i] == " ": # Check if the coordinate is a mine
                            apparent_board = reveal_empty(board, apparent_board, col + i, row + j)

    
    return apparent_board
    
# Check if the user has won
def check_win(apparent_board, real_board):
    for i in range(len(apparent_board)):
        for j in range(len(apparent_board[0])):
            if apparent_board[i][j] == "*" and real_board[i][j] != "M":
                return False
    return True

# Reveal all mines on the board
def reveal_mines(apparent_board, real_board):
    for i in range(len(real_board)):
        for j in range(len(real_board[0])):
            if real_board[i][j] == "M":
                apparent_board[i][j] = "M"
    return apparent_board

# Run the game
def minesweeper():
    difficulty = get_difficulty()
    apparent_board, real_board, flags = generate_boards(difficulty)
    print()
    print_instructions()
    
    max_col = len(real_board[0])
    max_row = len(real_board)
    
    mine_hit = False
    won = False
    
    while not mine_hit and not won:
        print(f"\nFlags left: {flags}")
        # display_board(real_board)
        display_board(apparent_board)
        col, row, flag = get_user_action(max_col, max_row)
        if col == None:
            break
        if type(apparent_board[row][col]) == int or apparent_board[row][col] == " ":
            print("This coordinate has already been revealed!")
        elif flag:
            if flags == 0:
                print("You have no flags left!")
            elif apparent_board[row][col] == "*":
                apparent_board[row][col] = "F"
                flags -= 1
            else:
                apparent_board[row][col] = "*"
                flags += 1
        elif apparent_board[row][col] == "F":
            print("This coordinate is flagged!")
        else:
            if real_board[row][col] == "M":
                mine_hit = True
            else:
                apparent_board[row][col] = " "
                apparent_board = reveal_empty(real_board, apparent_board, col, row)
                won = check_win(apparent_board, real_board)
                
    if mine_hit:
        print("You hit a mine!")
        apparent_board = reveal_mines(apparent_board, real_board)
        display_board(apparent_board)
    elif won:
        print("You win!")
        apparent_board = reveal_mines(apparent_board, real_board)
        display_board(apparent_board)
        
if __name__ == "__main__":    
    minesweeper()