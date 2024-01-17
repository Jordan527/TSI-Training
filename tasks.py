# Task 1
# print("Hello Jordan!\nI first learned python in year 12\nI have a really messed up back right now")

# Task 2
# name = "Jordan"
# age = 22
# print(f'Hello {name}, you are {age} years old')

# Task 3
# values = [14, "Y", "Hello!", 2.5, 306, -1, 4380000, False]
# for i in range(len(values)):
#     print(f"Question {i + 1}: {values[i]} is {type(values[i])}")


# Task 4

# Task 4.1
# x = 50
# y = 50
# if x > y:
#     print("Greater")

# Task 4.2
# x = 50
# y = 50
# if x == y:
#     print("Equal")
    
# Task 4.3
# def equalFunction(x, y):
#     if x == y:
#         print("Equal")
#     else:
#         print("Unequal")

# equalFunction(50, 50)
# equalFunction(51, 49)

# Task 4.4
# def operationFunction(x, y):
#     if x == y:
#         print(1)
#     elif x > y:
#         print(2)
#     else:
#         print(3)
        
# operationFunction(50, 50)
# operationFunction(57, 50)
# operationFunction(5, 50)

# Task 5
# def matchFunction(day):
#     match day:
#         case 1:
#             print("Saturday")
#         case 2:
#             print("Sunday")
#         case _:
#             print("Weekday")

# matchFunction(2)
# matchFunction(4)


# Task 6.1
# i = 0
# while i < 6:
#     print(i)
#     i += 1
    
# Task 6.2
# for i in range(6):
#     print(i)
#     if i == 3:
#         break

# Task 6.3
# i = 3
# while i <= 8:
#     if not i == 6:
#         print(i)
#     i += 1

# Task 6.4
# list1 = [1, 2, 3, 4, 5]
# list2 = ["apple", "banana", "cherry"]

# for num in list1:
#     for fruit in list2:
#         print(f"{num}, {fruit}")
        
# Task 7
def getTotal(num1, num2):
    return num1 + num2

print(getTotal(3, 5))
    