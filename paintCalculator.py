# Ensures the input is a valid number
def getValidNumber(value):
    while not value.isnumeric():
        value = input(f"please enter a valid number: ")
    return int(value)

# Get the size value of a given dimension
def getSize(dimension):
    size = input(f"{dimension}? ").strip()
    return getValidNumber(size)

# Get the number of coats wanted per user
def getCoats():
    options = (1, 2, 3)
    
    coats = input("How many coats of paint do you want? ").strip()
    coats = getValidNumber(coats)
    
    while coats not in options:
        coats = input(f"The number of coats must be between 1 and 3: ")
        coats = getValidNumber(coats)

    return coats

def getGaps(roomIndex, wallIndex):
    gaps = input("How many doors/windows does this wall have? ")
    gaps = getValidNumber(gaps)
    
    totalArea = 0
    
    for i in range (gaps):
        print(f"Room {roomIndex}, Wall {wallIndex}, Door/Window {i+1}")
        width = getSize("Width")
        height = getSize("Height")
        totalArea += width * height
        print()
        
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
    walls = getValidNumber(walls)
    print()
    
    totalArea = 0
    for i in range(walls):
        totalArea += getWall(roomIndex, i+1)
        print()
    
    return totalArea
       
# Calculate the area between all rooms 
def getTotalArea():
    rooms = input("How many rooms need painting? ")
    rooms = getValidNumber(rooms)
    print()
    
    totalArea = 0
    for i in range(rooms):
        totalArea += getRoom(i+1)
        print()
    
    return totalArea
    

# TODO: multiple rooms

area = getTotalArea()
litresByArea = round(area / 10, 2) # 10m^2 per litre based on B&Q paint calculator

coats = getCoats()
litresByCoats = litresByArea * coats
print(f"Litres: {litresByCoats}")
