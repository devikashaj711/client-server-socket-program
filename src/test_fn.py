import json

try:
    with open("data.json", "r") as file:
        current_data = json.load(file)
except:
    current_data = [] 
    print("new file")
# print("current_data")
# print(current_data)

for item in current_data:
    # print(item)
    # print("HAHAHA")

    print(item["id"], "\t", item["first name"], "", item["last_name"], "\t", item["phone_number"])
    
    # break

