import json
from budget import category

file_path = 'Ledger.json'
# read the ledger json file if it exits, creates one if it doesn't
try:
    with open(file_path, 'r') as file_handle:
        print('success')
        budget_dict = json.load(file_handle)
        print(file_handle.tell())
except Exception as err:
# creates a new one when the file doesn't exist
    print(err)
    with open(file_path, 'a') as file_handle:
        print(f"file didn't exist or unable to read the json file. Create a new one")
        budget_dict = dict()

# print the first five lines of the file:
# ledger_data = json.load(file_handle)

while True:
    category_input = input('Please enter a category (e.g., food or entertainment) or enter done to quit:')
    # convert input to lower case
    category_input = category_input.lower()
    if category_input == 'done':
        print('You have completed all the tasks')
        break
    # if the category already exists
    if category_input in budget_dict.keys():
        amount = budget_dict[category_input][0]['total']
        budget_item = category(category_input,amount)
    # if this is the first time creating the list or the category doesn't exist
    else:
        amount = input('This category does not exist. Enter a opening balance to create:')
        amount = float(amount)
        budget_item = category(category_input, amount)



