def getWidth():
    width = input("What is the width of your wall in cm: ").strip()
    while not width.isnumeric():
        width = input("Please enter a valid width: ")
    print()
    return int(width) / 100

def getHeight():
    height = input("What is the height of your wall in cm: ").strip()
    while not height.isnumeric():
        height = input("Please enter a valid height: ")
    print()
    return int(height) / 100

width = getWidth()
height = getHeight()
area = width * height

litres = round(area / 10, 2) # 10m^2 per litre based on B&Q paint calculator
print(litres)