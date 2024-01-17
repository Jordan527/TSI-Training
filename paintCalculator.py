# Ensures the input is a valid number
def getValidNumber(value):
    while not value.isnumeric():
        value = input(f"please enter a valid number: ")
    print()
    return int(value)

# Get the size value of a given dimension
def getSize(dimension, item):
    size = input(f"What is the {dimension} of your {item} in meters? ").strip()
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

def getGaps():
    gaps = input("How many doors/windows does this wall have? ")
    gaps = getValidNumber(gaps)
    
    totalArea = 0
    
    for i in range (gaps):
        print(f"Door/Window {i+1}")
        width = getSize("width", "door/window")
        height = getSize("height", "door/window")
        totalArea += width * height
        
    return totalArea
        
        
# TODO: multiple walls
# TODO: multiple rooms
width = getSize("width", "wall")
height = getSize("height", "wall")
gaps = getGaps()

area = (width * height) - gaps
litresByArea = round(area / 10, 2) # 10m^2 per litre based on B&Q paint calculator

coats = getCoats()
litresByCoats = litresByArea * coats
print(f"Litres: {litresByCoats}")
