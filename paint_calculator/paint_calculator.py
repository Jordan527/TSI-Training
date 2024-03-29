import math

# Ensures the input is a valid integer
def getValidInteger(value):
    while not is_integer(value):
        value = input("Please enter a whole number: ").strip()
    return int(value)

# Check if a string is a valid positive integer
def getValidPositiveIntiger(value):
    while not is_integer(value) or int(value) < 0:
        value = input("Please enter a whole number greater than 0: ").strip()
    return int(value)

# Checks if a string is a float value
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# Checks if a string is an integer value
def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

# Check if a size based input is in the correct format
def getValidSize(value):
    while (not is_float(value) or (not is_integer(value) and len(value.rsplit('.')[-1]) > 2)) or float(value) <= 0:
        value = input(f"please enter a valid number greater than 0 with at most 2 decimal places: ")
    return float(value)

# Get the size value of a given dimension
def getSize(dimension):
    size = input(f"{dimension} (meters)? ").strip()
    return getValidSize(size)

# Get the number of coats wanted per user
def getCoats():
    options = (1, 2, 3)

    coats = input("\nHow many coats of paint do you want? ").strip()
    coats = getValidInteger(coats)

    while coats not in options:
        coats = input(f"The number of coats must be between 1 and 3: ").strip()
        coats = getValidInteger(coats)

    return coats

# Calculate the area of all doors/windows in a room
def getTotalGapsArea(roomIndex, wallIndex):
    # TODO: allow for different shaped obstruction
    gaps = input("\nHow many doors/windows/obstructions does this wall have? ").strip()
    gaps = getValidPositiveIntiger(gaps)

    totalArea = 0

    for i in range(gaps):
        print(f"\nRoom {roomIndex}, Wall {wallIndex}, Door/Window/Obstruction {i+1}")
        width = getSize("Width")
        height = getSize("Height")
        totalArea += width * height

    return totalArea

# Calculate the area of a wall
def getWallArea(roomIndex, wallIndex):
    print(f"\nRoom {roomIndex}, Wall {wallIndex}")
    width = getSize("Width")
    height = getSize("Height")
    gaps = getTotalGapsArea(roomIndex, wallIndex)

    return (width * height) - gaps

# Calculate the area of a room
def getRoomArea(roomIndex):
    print(f"\nRoom {roomIndex}")
    walls = input("How many walls need painting? ").strip()
    walls = getValidPositiveIntiger(walls)

    totalArea = 0
    for i in range(walls):
        totalArea += getWallArea(roomIndex, i+1)

    return totalArea

# Calculate the total area between all rooms
def getTotalArea():
    rooms = input("How many rooms need painting? ").strip()
    rooms = getValidPositiveIntiger(rooms)

    totalArea = 0
    for i in range(rooms):
        totalArea += getRoomArea(i+1)

    return totalArea

# Get the users desired paint brand
def getBrandSuggestion(paints, volume):
    print("\nWhich brand of paint would you like to choose? \n0. Any")
    paintList = list(paints) # convert dictionary to list of keys
    paintOptions = list(range(len(paintList) + 1)) # get list of possible user inputs
    for i in range(len(paintOptions) - 1):
        canOptions = paints[paintList[i]]
        averages = 0
        for option in canOptions:
            averages += (1 / option[0]) * option[1]
        averages /= len(option)
        
        # TODO: Give an output of all paint options per brand, not just the average cost per litre
        print(f"{i+1}. {paintList[i]}: average of £{round(averages, 2)} per litre")

    brand = input("Choice: ").strip()
    brand = getValidInteger(brand)
    while brand not in paintOptions:
        brand = input("Please choose a valid option: ").strip()
        brand = getValidInteger(brand)
    return paintList[brand-1] if brand != 0 else None

# Generate paint suggestions
def getPaintSuggestion(paints, desiredBrand, volume):
    # TODO: Need to find the best combination of containers for the lowest cost, not just the cheapest outcome
    lowestCost = 0
    suggestion = []

    if desiredBrand:
        for option in paints[desiredBrand]:
            optionLitres = option[0]
            optionCost = option[1]

            containers = math.ceil(volume / optionLitres)
            cost = containers * optionCost
            if lowestCost == 0 or lowestCost > cost:
                lowestCost = cost
                suggestion = [desiredBrand, optionLitres, containers]
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


if __name__ == "__main__":
    print("""
Welcome to the Console Paint Calculator! 
This handy tool is designed to make your painting projects a breeze by providing quick and easy calculations for the amount of paint you'll need. 
Whether you're sprucing up a room or tackling a larger project, our console-based calculator will help you determine the right amount of paint, 
saving you time and ensuring a smooth painting experience. Let's get started on transforming your space with the perfect amount of paint!
    """)

    # TODO: have soft and hard limit for the number of rooms, walls and obstructions
    area = getTotalArea()
    litresByArea = area / 10 # 1 litre per 10m^2 based on B&Q and homebase paint calculators

    if litresByArea > 0:
        coats = getCoats()
        litresByCoat = litresByArea * coats

        wastage = input("\nInclude 10% wastage?(Y/N)\nIt is recommended to purchase at least 10% extra product to allow for errors and damages\n").strip()
        while "y" not in wastage.lower() and "n" not in wastage.lower():
            wastage = input("Please enter 'Y' or 'N': ")

        if 'y' in wastage.lower():
            litresByCoat *= 1.1

        litres = round(litresByCoat, 2)
        
        # (litres, cost)
        paints = {
            "Dulux": ((1, 17), (2.5, 22), (5, 34)),
            "Dulux Trade": ((1, 20), (2.5, 34), (5, 60)),
            "Crown": ((1, 20.56), (2.5, 27.42), (5, 56.44)),
        }

        brand = getBrandSuggestion(paints, litres)
        suggestion, cost = getPaintSuggestion(paints, brand, litres)
        
        brand = suggestion[0]
        volume = suggestion[1]
        cans = suggestion[2]
        
        print(f"\nTo cover this area, you need {litres} litre{"s" if litres != 1 else ""} of paint")
        print(f"\nIt is suggested that you buy {cans} can{"s" if cans > 1 else ""} of {volume}L {brand} paint for £{cost}")
    else:
        print(f"\nYou do not need to buy any paint")
