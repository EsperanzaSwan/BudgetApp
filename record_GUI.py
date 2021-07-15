import tkinter as tk
import json
from budget import category





def check_ledger(category):
    # if the category already exists
    if category in budget_file.keys():
        amount = budget_file[category][0]['total']
        # retrieve all the previous ledgers
        item_ledger = budget_file[category][1:]
        # create the budget object
        the_item = category(category, amount)
        # if this is the first time creating the ledger or the category doesn't exist
    else:
        amount = input('This category does not exist. Enter amount to create one or enter done to quit:')
        if not amount.isnumeric():
            return False
        amount = float(amount)
        item_ledger = []
        the_item = category(category, amount)
    print(the_item, item_ledger)



root = tk.Tk()
# setting the windows size
root.title('Budget App')
root.geometry("600x400")
category_label = tk.Label(root, text = 'Please enter a category (e.g., food):', font=('calibre',12, 'bold'))

category_button = tk.Button(root, text = "Confirm", fg = "red", command=check_ledger('Health'))
# category = tk.StringVar()
category_label.grid()
category_button.grid(column=1, row=0)

root.mainloop()
