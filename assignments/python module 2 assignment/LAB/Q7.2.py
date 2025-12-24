# merging two lists into one dictionary using a loop
keys_list = ["name", "age", "gender"]
values_list = ["Sam", 25, "Male"]

merged_dict = {}

for i in range(len(keys_list)):
    merged_dict[keys_list[i]] = values_list[i]

print("Merged Dictionary:", merged_dict)