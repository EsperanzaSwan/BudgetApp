import tkinter as tk
from tkinter import ttk
import json
from budget import category
from functools import partial

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Budget App')
        self.geometry('500x600+500+500')
        self.columnconfigure(0, weight = 2)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)

        self.category_input()

    def category_input(self):
        padding = {'padx': 5, 'pady': 5}

        # label for category
        ttk.Label(self, text = "Please enter a category (e.g., food):").grid(column = 0, row = 0, **padding)

        # category entry
        self.category_var = tk.StringVar()
        self.category_entry = ttk.Entry(self, textvariable = self.category_var)
        self.category_entry.grid(column = 1, row = 0, **padding)
        self.category_entry.focus()

        # category button
        self.category_button = ttk.Button(self, text = 'Confirm', command = self.check_ledger)
        self.category_button.grid(column = 2, row = 0, **padding)

        # output label
        self.c_output_label = ttk.Label(self)
        self.c_output_label.grid(column = 0, row = 1, **padding)

    def check_ledger(self):
        # load the previous created ledger
        global budget_dict, stored_ledger

        category_input = self.category_var.get()
        category_input = category_input.strip()
        category_input = category_input.lower()
        print(f'category is {category_input}')
        # if the category already exists
        if category_input in budget_dict.keys():
            amount = budget_dict[category_input][0]['total']
            # retrieve all the previous ledgers
            stored_ledger = budget_dict[category_input][1:]
            # create the budget object
            self.record_item = category(category_input, amount)
            # if this is the first time creating the ledger or the category doesn't exist
            self.c_output_label.config(text = f'{category_input}: current balance is {amount} dollars')
        else:
            print(f'category_entry is {category_input}')
            amount = input('The category does not exist. Enter amount to create one or done to quit:')
            if not amount.isnumeric():
                return False
            amount = float(amount)
            stored_ledger = []
            self.record_item = category(category_input, amount)


if __name__ == "__main__":
    global budget_dict, stored_ledger
    file_path = 'Ledger.json'

    try:
        with open(file_path, 'r') as file_handle:
            budget_dict = json.load(file_handle)
    except Exception as err:
        # print(err)
        budget_dict = dict()
    app = BudgetApp()
    app.mainloop()