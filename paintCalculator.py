# Ensures the input is a valid number
def getValidInteger(value):
    while not value.isnumeric():
        value = input(f"please enter a valid number: ")
    return int(value)

# Checks if a string is a float value
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def getValidSize(value):
    while (not is_float(value) or len(value.rsplit('.')[-1]) > 2) or float(value) <= 0:
        value = input(f"please enter a valid number greater than 0 with at most 2 decimal places: ")
    return float(value)

# Get the size value of a given dimension
def getSize(dimension):
    size = input(f"{dimension}? ").strip()
    return getValidSize(size)

# Get the number of coats wanted per user
def getCoats():
    options = (1, 2, 3)
    
    coats = input("How many coats of paint do you want? ").strip()
    coats = getValidInteger(coats)
    
    while coats not in options:
        coats = input(f"The number of coats must be between 1 and 3: ")
        coats = getValidInteger(coats)

    return coats

def getGaps(roomIndex, wallIndex):
    gaps = input("How many doors/windows does this wall have? ")
    gaps = getValidInteger(gaps)
    
    totalArea = 0
    
    for i in range (gaps):
        print()
        print(f"Room {roomIndex}, Wall {wallIndex}, Door/Window {i+1}")
        width = getSize("Width")
        height = getSize("Height")
        totalArea += width * height
        
    return totalArea

# Calculate the area of a wall
def getWall(roomIndex, wallIndex):
    print(f"Room {roomIndex}, Wall {wallIndex}")
    width = getSize("Width")
    height = getSize("Height")
    print()
    gaps = getGaps(roomIndex, wallIndex)

    return (width * height) - gaps

# Calculate the area of a room  
def getRoom(roomIndex):
    print(f"Room {roomIndex}")
    walls = input("How many walls need painting? ")
    walls = getValidInteger(walls)
    
    totalArea = 0
    for i in range(walls):
        print()
        totalArea += getWall(roomIndex, i+1)
    
    return totalArea
       
# Calculate the area between all rooms 
def getTotalArea():
    rooms = input("How many rooms need painting? ")
    rooms = getValidInteger(rooms)
    
    totalArea = 0
    for i in range(rooms):
        print()
        totalArea += getRoom(i+1)
    
    return totalArea
    

area = getTotalArea()
print()
litresByArea = area / 10 # 10m^2 per litre based on B&Q paint calculator

coats = getCoats()
print()
litresToClean = litresByArea * coats

wastage = input("Include 10% wastage?(Y/N)\nIt is recommended to purchase at least 10% extra product to allow for errors and damages\n").strip()
while "y" not in wastage.lower() and "n" not in wastage.lower():
    wastage = input("Please enter 'Y' or 'N'")

if 'y' in wastage.lower():
    litresToClean *= 1.1
        

litres = round(litresToClean, 2) if litresToClean > 0 else 0
print(f"Litres: {litres}")
