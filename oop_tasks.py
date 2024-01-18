class Car:
    def __init__(self, model, color):
        self.model = model
        self.color = color
        
    def print_info(self):
        print("Model: " + self.model)
        print("Color: " + self.color)
     
my_car = Car("Benz", "Red")
my_car.print_info()