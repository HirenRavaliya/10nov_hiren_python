#converting two lists into one dictionary using a for loop
keys = ["name", "age", "role"]
values = ["hiren", 22, "developer"]
new_dict = {}

for i in range(len(keys)):
    new_dict[keys[i]] = values[i]

print("Merged Dictionary:", new_dict)