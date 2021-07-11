import json
from budget import category

# "check_numeric" checks if the input is a numeric value
def check_numeric(screen_prompt):
    user_input = ''
    while len(user_input) < 1 or not user_input.isnumeric():
        if len(user_input) < 1:
            user_input = input(screen_prompt)
        else:
            print(f'You entered {user_input}. Please enter a numeric value.')
            user_input = input(screen_prompt)
    return user_input

# "check_ledger" checks if a category is already in the ledger and creates the object accordingly
def check_ledger(item_category, budget_dict):
    # if the category already exists
    if item_category in budget_dict.keys():
        amount = budget_dict[item_category][0]['total']
        # retrieve all the previous ledgers
        item_ledger = budget_dict[item_category][1:]
        # create the budget object
        the_item = category(item_category, amount)
    # if this is the first time creating the ledger or the category doesn't exist
    else:
        amount = check_numeric('This category does not exist. Enter a opening balance to create:')
        amount = float(amount)
        the_item = category(category_input, amount)
        item_ledger = []
    return the_item, item_ledger

# append previous ledger
def append_ledger(item, ledger_history):
    if len(ledger_history) > 0:
        for each_item in ledger_history:
            item.ledger.append(each_item)


file_path = 'Ledger.json'
# read the ledger json file if it exits, creates one if it doesn't
try:
    with open(file_path, 'r') as file_handle:
        print('success')
        budget_dict = json.load(file_handle)
        print(file_handle.tell())
except Exception as err:
    print(err)
    # there is no need to create a file if file doesn't exist, because I will need to update
    # the entire json file at the end
    # with open(file_path, 'a') as file_handle:
    #     print(f"file didn't exist or unable to read the json file. Create a new one")
    budget_dict = dict()

while True:
    category_input = input('Please enter a category (e.g., food or entertainment) or enter done to quit: ')
    # remove white space at the beginning and the end and convert input to lower case
    category_input = category_input.strip()
    category_input = category_input.lower()
    if category_input == 'done':
        print('You have completed all the tasks.')
        break
    # if the category already exists
    [record_item, stored_ledger] = check_ledger(category_input, budget_dict)


    while True:
        action_input = check_numeric('Please choose 1. deposit 2. withdraw 3. transfer 4. get balance 5. print statement 6. quit:')
        action_input = int(action_input)
        # deposit
        if action_input == 1:
            deposit_amount = check_numeric('Please enter deposit amount:')
            deposit_amount = float(deposit_amount)
            deposit_description = input('Please enter the description for the deposit:')
            record_item.deposit(deposit_amount, deposit_description)
        # withdraw
        elif action_input == 2:
            withdraw_amount = check_numeric('Please enter withdraw amount:')
            withdraw_amount = float(withdraw_amount)
            withdraw_description = input('Please enter the description for the withdraw:')
            success_or_not = record_item.withdraw(withdraw_amount, withdraw_description)
            if success_or_not is False:
                print(f"{record_item.category} only has {record_item.ledger[0]['total']} dollars. Withdraw failed.")
        # transfer
        elif action_input == 3:
            transfer_category = input('Please enter a category to transfer from:')
            transfer_category = transfer_category.strip()
            transfer_category = transfer_category.lower()
            [transfer_item, transfer_item_ledger] = check_ledger(transfer_category, budget_dict)
            transfer_amount = float(check_numeric('Please enter transfer amount:'))
            success_or_not = record_item.transfer(transfer_amount, transfer_item)
            # not enough funds. Transfer failed
            if success_or_not is False:
                print(f"{transfer_item.category} only has {transfer_item.ledger[0]['total']} dollars. Transfer failed.")
            # transfer successful, update transfer item's ledger as well
            else:
                append_ledger(transfer_item, transfer_item_ledger)
                budget_dict[transfer_item.category] = transfer_item.ledger

        else:
            print(f'You have completed all the action for {category_input}')
            break

    # append previous ledger to the updated ledger
    append_ledger(record_item, stored_ledger)
    # update the category
    budget_dict[record_item.category] = record_item.ledger

# I need to update the entire file because I can't save multiple json objects, in other words, I can't
# append the file. This will need improvement in the future, but will serve the purpose for right now.
with open(file_path, 'w') as file_handle:
    json.dump(budget_dict, file_handle)


