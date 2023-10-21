# Sample list
my_list = [1, 2, 3, 4, 5]

# Tuples with (item_to_find, item_to_replace)
replace_tuples = [(2, 20), (4, 40), (5, 50)]

# Loop through the list
for i, item in enumerate(my_list):
    for item_to_find, item_to_replace in replace_tuples:
        if item == item_to_find:
            my_list[i] = item_to_replace

print(my_list)
