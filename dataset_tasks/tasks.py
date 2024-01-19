# # Task 1
# yearResults = {
#     "Jordan": (67, 32, 75, 49),
#     "Sam": (48, 12, 49, 70),
#     "Steve": (31, 84, 19, 70),
# }

# for student, results in yearResults.items(): 
#     print(f"The best grade for {student} is {max(results)}")
    
# # Task 2
# yearAverages = {key:(sum(value)/len(value)) for (key, value) in yearResults.items()}
# print()
# for student, average in yearAverages.items():
#     print(f"The average grade for {student} is {average}")
    
# # Task 3
# from collections import deque
# queue = deque([2, 5, 3, 1])

# def reverseQueue(input):
#     reversedInput = deque(reversed(input))
#     for i in range(len(input)):
#         input.popleft()
#         input.append(reversedInput[i])
    
# print(queue)
# reverseQueue(queue)
# print(queue)

# # Task 4
# from collections import ChainMap

# def addProduct(history, product, price):
#     latest = history.maps[0]
#     if product in latest:
#         history = history.new_child({product: price})
#     else:
#         history[product] = price
        
#     return history

# dict1 = {"Apples": 25, "Pears": 15}
# dict2 = {"Peaches": 2, "Apples": 3}
# history = ChainMap(dict2, dict1)

# print(history)
# history = addProduct(history, "Pears", 8)
# print(history)
# history = addProduct(history, "Pears", 17)
# print(history)

# # Task 5
# import json
# import csv
# import os

# for root, dirs, files in os.walk(os.getcwd()):
#     for name in files:
#         if name.endswith((".json")):
#             f = open(name)
#             data = json.load(f)
#             f.close()
            
#             fileName = name.split('.')[0]
#             csvName = fileName + ".csv"
#             with open(csvName, 'w', newline='') as file:
#                 writer = csv.writer(file)
#                 field = data[0].keys()
                
#                 writer.writerow(field)
#                 for row in data:
#                     writer.writerow(row.values())
                    
#                 file.close()