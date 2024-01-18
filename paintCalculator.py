import math
# Ensures the input is a valid integer
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
    
    coats = input("\nHow many coats of paint do you want? ").strip()
    coats = getValidInteger(coats)
    
    while coats not in options:
        coats = input(f"The number of coats must be between 1 and 3: ")
        coats = getValidInteger(coats)

    return coats

# Calculate the area of all doors/windows in a room
def getGaps(roomIndex, wallIndex):
    gaps = input("\nHow many doors/windows does this wall have? ")
    gaps = getValidInteger(gaps)
    
    totalArea = 0
    
    for i in range (gaps):
        print(f"\nRoom {roomIndex}, Wall {wallIndex}, Door/Window {i+1}")
        width = getSize("Width")
        height = getSize("Height")
        totalArea += width * height
        
    return totalArea

# Calculate the area of a wall
def getWall(roomIndex, wallIndex):
    print(f"\nRoom {roomIndex}, Wall {wallIndex}")
    width = getSize("Width")
    height = getSize("Height")
    gaps = getGaps(roomIndex, wallIndex)

    return (width * height) - gaps

# Calculate the area of a room  
def getRoom(roomIndex):
    print(f"\nRoom {roomIndex}")
    walls = input("How many walls need painting? ")
    walls = getValidInteger(walls)
    
    totalArea = 0
    for i in range(walls):
        totalArea += getWall(roomIndex, i+1)
    
    return totalArea
       
# Calculate the total area between all rooms 
def getTotalArea():
    rooms = input("How many rooms need painting? ")
    rooms = getValidInteger(rooms)
    
    totalArea = 0
    for i in range(rooms):
        totalArea += getRoom(i+1)
    
    return totalArea

def getBrandSuggestion(paints, volume):
    # TODO: Give cost insight for each brand
    print("\nWhich brand of paint would you like to choose?\n0. Any")
    paintList = list(paints)
    options = list(range(len(paintList) + 1))
    for i in range(len(options) - 1):
        print(f"{i+1}. {paintList[i]}")
        
    brand = input()
    brand = getValidInteger(brand)
    
    while brand not in options:
        brand = input("Please choose a valid option: ")
        brand = getValidInteger(brand)
    return paintList[brand-1] if brand != 0 else None

# Generate paint suggestions
def getPaintSuggestion(paints, brand, volume):    
    lowestCost = 0
    suggestion = []
    
    if brand:
        for option in paints[brand]:
            optionLitres = option[0]
            optionCost = option[1]
            
            containers = math.ceil(volume / optionLitres)
            cost = containers * optionCost
            if lowestCost == 0 or lowestCost > cost:
                lowestCost = cost
                suggestion = [brand, optionLitres, containers]
    else:
        for brand in paints:
            options = paints[brand]
            for option in options:
                optionLitres = option[0]
                optionCost = option[1]
                
                containers = math.ceil(volume / optionLitres)
                cost = containers * optionCost
                if lowestCost == 0 or lowestCost > cost:
                    lowestCost = cost
                    suggestion = [brand, optionLitres, containers]
    
    return suggestion, lowestCost
            
    
    

area = getTotalArea()
litresByArea = area / 10 # 10m^2 per litre based on B&Q paint calculator

coats = getCoats()
litresToClean = litresByArea * coats

wastage = input("\nInclude 10% wastage?(Y/N)\nIt is recommended to purchase at least 10% extra product to allow for errors and damages\n").strip()
while "y" not in wastage.lower() and "n" not in wastage.lower():
    wastage = input("Please enter 'Y' or 'N'")

if 'y' in wastage.lower():
    litresToClean *= 1.1
        

litres = round(litresToClean, 2) if litresToClean >= 0 else 0

if litres > 0:  
    # (litres, cost)
    paints = {
        "Dulux": ((2.5, 22), (5, 34)),
        "GoodHome": ((0.05, 2.25), (2.5, 16), (5, 22)),
        "Laura Ashley": ((0.1, 5), (2.5, 42), (5, 74)),
    }
    
    print(f"\nTo cover this area, you need {litres} litres of paint")
    brand = getBrandSuggestion(paints, litres)
    suggestion, cost = getPaintSuggestion(paints, brand, litres)
    brand = suggestion[0]
    volume = suggestion[1]
    cans = suggestion[2]
    print(f"\nIt is suggested that you buy {cans} can{"s" if cans > 1 else ""} of {volume if volume >= 1 else int(volume * 1000)}{"L" if volume >= 1 else "ml"} {brand} paint for £{cost}")
else:
    print(f"\nYou do not need to buy any paint")