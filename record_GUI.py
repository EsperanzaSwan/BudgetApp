import tkinter as tk
from tkinter import ttk
import json
from budget import category
from functools import partial

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Budget App')
        self.geometry('700x600+500+500')
        self.columnconfigure(0, weight = 2)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.create_widgets()

    def create_widgets(self):
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


        # despoist label
        ttk.Label(self,text = 'Deposit: Enter a deposit amount').grid(column = 0, row = 3, **padding)
        # deposit entry
        self.deposit_amount = tk.StringVar()
        self.deposit_entry = ttk.Entry(self, textvariable = self.deposit_amount)
        self.deposit_entry.grid(column = 1, row =3, **padding)
        self.deposit_entry.focus()
        # despoist button
        self.despoist_button = ttk.Button(self, text='Confirm', command=self.deposit)
        self.despoist_button.grid(column = 2, row = 3, **padding)


    def check_ledger(self):
        global budget_dict, stored_ledger

        category_input = self.category_var.get()
        category_input = category_input.strip()
        self.category_input = category_input.lower()
        print(f'category is {self.category_input}')
        # if the category already exists
        if self.category_input in budget_dict.keys():
            amount = budget_dict[self.category_input][0]['total']
            # retrieve all the previous ledgers
            stored_ledger = budget_dict[self.category_input][1:]
            # create the budget object
            self.record_item = category(self.category_input, amount)
            self.c_output_label.config(text = f'{self.category_input}: current balance is {amount} dollars')
        # if this is the first time creating the ledger or the category doesn't exist
        else:
            self.c_output_label.config(text=f"The category doesn't exist. Enter amount to create or done to quit:")
            self.amount_var = tk.StringVar()
            # amount entry
            self.amount_entry = ttk.Entry(self, textvariable = self.amount_var)
            self.amount_entry.grid(column = 1, row = 1)
            self.amount_entry.focus()
            #amount button
            self.amount_button = ttk.Button(self, text = 'Confirm', command = self.create_category)
            self.amount_button.grid(column = 2, row = 1)

    def create_category(self):
        global stored_ledger
        amount = self.amount_var.get()
        amount = amount.strip()
        amount = amount.lower()
        if amount == 'done':
            self.amount_entry.destroy()
            self.amount_button.destroy()
            return False
        elif not amount.isnumeric():
            self.c_output_label.config(text=f"You entered {amount}. Enter a number or done to quit:")
        amount = float(amount)
        stored_ledger = []
        self.record_item = category(self.category_input, amount)
        self.c_output_label.config(text=f'{self.category_input}: current balance is {amount} dollars')
        self.amount_entry.destroy()
        self.amount_button.destroy()

    def deposit(self):
        print('Hi')


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