# Ensures the input is a valid number
def getValidNumber(value, item):
    while not value.isnumeric():
        value = input(f"please enter a valid {item}: ")
    return int(value)

# Get the size value of a given dimension
def getSize(dimension, item):
    size = input(f"What is the {dimension} of your {item} in meters? ").strip()
    return getValidNumber(size, dimension)

# Get the number of coats wanted per user
def getCoats():
    options = (1, 2, 3)
    
    coats = input("How many coats of paint do you want? ").strip()
    if coats.isnumeric():
        coats = int(coats)
    
    while coats not in options:
        coats = input(f"please enter a valid number between 1 and 3: ")
        if coats.isnumeric():
            coats = int(coats)

    return coats

width = getSize("width", "wall")
height = getSize("height", "wall")

area = width * height
litresByArea = round(area / 10, 2) # 10m^2 per litre based on B&Q paint calculator

coats = getCoats()
litresByCoats = litresByArea * coats
print(litresByCoats)

# TODO: Door is 1.5m^2, double door is 3m^2