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
        amount = input('The category does not exist. Enter amount to create or enter done to quit:')
        if not amount.isnumeric():
            return False
        amount = float(amount)
        the_item = category(category_input, amount)
        item_ledger = []
    results = [the_item, item_ledger]
    return results

# load the previous created ledger
file_path = 'Ledger.json'
try:
    with open(file_path, 'r') as file_handle:
        budget_dict = json.load(file_handle)
except Exception as err:
    # print(err)
    budget_dict = dict()

while True:
    category_input = input('Please enter a category (e.g., food or entertainment) or enter done to quit: ')
    # remove white space at the beginning and the end and convert input to lower case
    category_input = category_input.strip()
    category_input = category_input.lower()
    if category_input == 'done':
        print('You have completed all the tasks.')
        break
    # check if the category already exits
    if not check_ledger(category_input, budget_dict):
        break
    else:
        [record_item, stored_ledger] = check_ledger(category_input, budget_dict)

    while True:
        action_input = check_numeric('Please choose 1. deposit 2. withdraw 3. transfer 4. print statement 5. quit:')
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
            if not check_ledger(transfer_category, budget_dict):
                break
            else:
                [transfer_item, transfer_item_ledger] = check_ledger(transfer_category, budget_dict)
            transfer_amount = float(check_numeric('Please enter transfer amount:'))
            success_or_not = record_item.transfer(transfer_amount, transfer_item)
            # not enough funds. Transfer failed
            if success_or_not is False:
                print(f"{transfer_item.category} only has {transfer_item.ledger[0]['total']} dollars. Transfer failed.")
            # transfer successful, update transfer item's ledger as well
            else:
                transfer_item.ledger = transfer_item.ledger + transfer_item_ledger
                budget_dict[transfer_item.category] = transfer_item.ledger

        elif action_input == 4:
            print(f"{record_item.category}: {record_item.ledger[0]['total']} dollars")
            temp_file = record_item.ledger[1:] + stored_ledger
            for statement in temp_file:
                print(statement)

        else:
            print(f'You have completed all the action for {category_input}')
            break

    # append previous ledger to the updated ledger
    record_item.ledger = record_item.ledger + stored_ledger
    # update the category
    budget_dict[record_item.category] = record_item.ledger

# I need to update the entire file because I can't save multiple json objects, in other words, I can't
# append the file. This will need improvement in the future, but will serve the purpose for right now.
with open(file_path, 'w') as file_handle:
    json.dump(budget_dict, file_handle)


