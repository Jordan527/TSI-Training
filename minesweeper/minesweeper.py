import random

def generate_array(width, height):
    global DEFAULT_VALUE
    return [[DEFAULT_VALUE for x in range(width)] for y in range(height)]
    

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

def generate_boards():
    match get_difficulty():
        case 1:
            apparent_board = generate_array(8, 8)
            real_board = generate_array(8, 8)
            real_board = place_bombs(real_board, 10)
            return apparent_board, real_board, 10
        case 2:
            apparent_board = generate_array(16, 16)
            real_board = generate_array(16, 16)
            real_board = place_bombs(real_board, 40)
            return apparent_board, real_board, 40
        case 3:
            apparent_board = generate_array(16, 30)
            real_board = generate_array(16, 30)
            real_board = place_bombs(real_board, 99)
            return apparent_board, real_board, 99

def display_board(board):
    print()
    for row in board:
        output = "|"
        for value in row:
            output += f" {value} |"
        print(output)

def get_user_action(max_col, max_row):
    while True:
        action = input("\nAction: ").strip()
        try:
            if action.lower() == 'help':
                print_instructions()
            else:
                valid = True
                
                parts = action.split(" ")
                col = int(parts[0])
                row = int(parts[1])
                
                if col < 1 or col > max_col:
                    print(f'Please enter a column value between 1 and {max_col}')
                    valid = False

                if valid and (row < 1 or row > max_row):
                    print(f'Please enter a row value between 1 and {max_row}')
                    valid = False
                
                if valid and len(parts) > 2:
                    if parts[2].lower() == "m":
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
        
def print_instructions(invalid_format=False):
    if invalid_format:
        print("\nPlease format your action according the instructions below:")
    print("1. To select a coordinate, enter the column and row (example: 2 3)")
    print("2. To flag a coordinate, enter the column and row, followed by 'M' (example: 2 3 M)")

def minesweeper():
    apparent_board, real_board, mines = generate_boards()
    
    max_col = len(real_board[0])
    max_row = len(real_board)
    terminated = False
    
    display_board(apparent_board)
    
    while not terminated:
        col, row, flag = get_user_action(max_col, max_row)
    
        

if __name__ == "__main__":
    DEFAULT_VALUE = "X"
    MINE_VALUE = "M"
    EMPTY_VALUE = " "
    FLAG_VALUE = "F"
    
    minesweeper()