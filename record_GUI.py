import tkinter as tk
from tkinter import ttk
import json
from budget import category

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Budget App')
        self.geometry('1000x500+250+200')
        self.columnconfigure(0, weight = 2)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.columnconfigure(4, weight=1)
        self.create_widgets()

    def create_widgets(self):
        # check theme
        padding = {'padx': 5, 'pady': 5}
        # create button style
        button_style = ttk.Style()
        button_style.configure('TButton', font = ('calibri', 12, 'bold'), highlightbackground = 'white',
                               highlightthickness = 0)

        # label for category
        ttk.Label(self, text = "Please enter a category (e.g., food):",
                  font = ('calibri', 12, 'bold')).grid(column = 0, row = 0, **padding)
        # category entry
        self.category_var = tk.StringVar()
        self.category_entry = ttk.Entry(self, textvariable = self.category_var)
        self.category_entry.grid(column = 1, row = 0, **padding)
        self.category_entry.focus()
        # category button
        self.category_button = ttk.Button(self, text = 'Confirm', style = 'TButton', command = self.check_ledger)
        self.category_button.grid(column = 2, row = 0, **padding)
        # output label
        self.c_output_label = ttk.Label(self)
        self.c_output_label.grid(column = 0, row = 1, **padding)


        # despoist label
        ttk.Label(self,text = 'Deposit: Enter a deposit amount:').grid(column = 0, row = 4, **padding)
        # deposit amount entry
        self.deposit_amount = tk.StringVar()
        self.deposit_entry = ttk.Entry(self, textvariable = self.deposit_amount)
        self.deposit_entry.grid(column = 1, row =4, **padding)
        self.deposit_entry.focus()
        # depoist description label
        ttk.Label(self,text = 'Enter description (e.g. pay check, optional):').grid(column = 2, row = 4, **padding)
        # deposit description entry
        self.deposit_description = tk.StringVar()
        self.deposit_description_entry = ttk.Entry(self, textvariable = self.deposit_description)
        self.deposit_description_entry.grid(column = 3, row =4, **padding)
        # despoist button
        self.deposit_button = ttk.Button(self, text='Confirm', style = 'TButton', command=self.deposit)
        self.deposit_button.grid(column = 4, row = 4, **padding)
        # deposit output label
        self.d_output_label = ttk.Label(self)
        self.d_output_label.grid(column = 0, row = 5, **padding)

        # withdraw label
        ttk.Label(self,text = 'Withdraw: Enter a withdrawl amount:').grid(column = 0, row = 6, **padding)
        # withdraw amount entry
        self.withdraw_amount = tk.StringVar()
        self.withdraw_entry = ttk.Entry(self, textvariable = self.withdraw_amount)
        self.withdraw_entry.grid(column = 1, row =6, **padding)
        self.withdraw_entry.focus()
        # withdraw description label
        ttk.Label(self,text = 'Enter description (e.g. buy food, optional):').grid(column = 2, row = 6, **padding)
        # deposit description entry
        self.withdraw_description = tk.StringVar()
        self.withdraw_description_entry = ttk.Entry(self, textvariable = self.withdraw_description)
        self.withdraw_description_entry.grid(column = 3, row =6, **padding)
        # despoist button
        self.withdraw_button = ttk.Button(self, text='Confirm', style = 'TButton', command=self.withdraw)
        self.withdraw_button.grid(column = 4, row = 6, **padding)
        # deposit output label
        self.w_output_label = ttk.Label(self)
        self.w_output_label.grid(column = 0, row = 7, **padding)

        # show statement
        self.statement_button = ttk.Button(self, text = 'Show Statement', style = 'TButton',
                                           command = self.statement)
        self.statement_button.grid(column = 0, row = 8, **padding)
        # self.s_output_label = ttk.Label(self)
        # self.s_output_label.grid(column=0, row=9, **padding)

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
            print(self.category_input)
            self.c_output_label.config(text = f'{self.category_input}: current balance is ${amount}')
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
        amount = self.deposit_amount.get()
        amount = amount.strip()
        amount = amount.lower()
        if not amount.isnumeric():
            self.d_output_label.config(text=f"You entered {amount}. Please enter a number:")
        amount = float(amount)
        description = self.deposit_description.get()
        self.record_item.deposit(amount, description)
        self.d_output_label.config(text=f"${amount} deposited to {self.record_item.category}")

    def withdraw(self):
        amount = self.withdraw_amount.get()
        amount = amount.strip()
        amount = amount.lower()
        if not amount.isnumeric():
            self.w_output_label.config(text=f"You entered {amount}. Please enter a number:")
        amount = float(amount)
        description = self.withdraw_description.get()
        self.record_item.withdraw(amount, description)
        if self.record_item.indicator is False:
            self.w_output_label.config(text=f"Withdrawl failed. {self.record_item.category}'s balance is ${self.record_item.ledger[0]['total']} ",
                                       font = ('calibri', 12, 'bold'))
        else:
            self.w_output_label.config(text=f"${amount} withdrawn from {self.record_item.category}")

    def statement(self):
        global stored_ledger
        statement_str = str()
        temp_file = self.record_item.ledger[1:] + stored_ledger
        print(temp_file)
        for each_item in temp_file:
            statement_str = statement_str + str(each_item) + '\n'
        message_len = len(temp_file)
        self.statement_message = tk.Message(self, text = statement_str)
        self.statement_message.grid(column = 0, row = 9)

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