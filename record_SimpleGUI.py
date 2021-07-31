import PySimpleGUI as sg
import json
from budget import category

global stored_ledger, record_item

# create statement window
def statement():
    global stored_ledger, record_item
    temp_file = record_item.ledger + stored_ledger
    file_size = len(temp_file)
    statement_str = str()
    for each_item in temp_file:
        statement_str = statement_str + str(each_item) + '\n'
    statement_str = statement_str.replace('{', '')
    statement_str = statement_str.replace('}', '')
    statement_str = statement_str.replace("'", '')
    print(statement_str)
    layout = [[sg.Text(statement_str, size = (70, file_size + 2), key='-QUERY-', font = ('calibri', 15, 'bold'))]]
    window2 = sg.Window('Statement', layout)
    while True:
        event, values = window2.read()
        if event == sg.WIN_CLOSED:
            break
    window2.close()


# load stored ledger
file_path = 'Ledger.json'
try:
    with open(file_path, 'r') as file_handle:
        budget_dict = json.load(file_handle)
except Exception as err:
    # print(err)
    budget_dict = dict()
# retrieve the exsiting categories
category_list = list(budget_dict.keys())

sg.theme('DarkAmber')
# define widgets
layout = [[sg.Text('Please choose a category or enter a new one:', font=('calibri', 15, 'bold')),
           sg.Combo(values=category_list, font=('calibri', 15), key='-CATEGORY-'),
           sg.Button(button_text='Confirm', font=('calibri', 13, 'bold'), key='-CCONFIRM-')],
          [sg.Text(size=(60, 1), font=('calibri', 15, 'bold'), key='-OUTPUT-')],
          [sg.Text('Deposit: Amount:', font=('calibri', 15, 'bold'), size = (14, 1)),
           sg.Input(font=('calibri', 15), key='-DAMOUNT-', size=(8, 1)),
           sg.Text('Description (optional)', font=('calibri', 15, 'bold'), size = (18,1)),
           sg.Input(font=('calibri', 15), key='-DDESCRIPTION-', size=(20, 1)),
           sg.Button(button_text='Confirm', font=('calibri', 13, 'bold'), key='-DCONFIRM-')],
          [sg.Text('Withdraw: Amount', font=('calibri', 15, 'bold'), size = (14, 1)),
           sg.Input(font=('calibri', 15), key='-WAMOUNT-', size=(8, 1)),
           sg.Text('Description (optional)', font=('calibri', 15, 'bold'), size = (18,1)),
           sg.Input(font=('calibri', 15), key='-WDESCRIPTION-', size=(20, 1)),
           sg.Button(button_text='Confirm', font=('calibri', 13, 'bold'), key='-WCONFIRM-')],
          [sg.Text('Transfer: Amount', font=('calibri', 15, 'bold'), size = (14, 1)),
           sg.Input(font=('calibri', 15), key='-TAMOUNT-', size=(8, 1)),
           sg.Text('Choose Category:', font=('calibri', 15, 'bold'), size = (18,1)),
           sg.Combo(values=category_list, font=('calibri', 15), key='-TDESCRIPTION-', size=(19, 1), readonly='True'),
           sg.Button(button_text='Confirm', font=('calibri', 13, 'bold'), key='-TCONFIRM-')],
          [sg.Button('Show Statement', pad=((220, 0), (15, 10)), font=('calibri', 13, 'bold'), key ='-SHOW-'),
            sg.Button('Save Changes', pad=((10, 0), (15, 10)), font=('calibri', 13, 'bold'), key ='-SAVE-')],
          [sg.Button('Exit', pad=((320, 0), (15, 10)), font=('calibri', 13, 'bold'))]]
window = sg.Window('Budget App', layout)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    elif event == '-CCONFIRM-':
        # check if the category exists
        category_input = values['-CATEGORY-']
        if len(category_input) < 1: # no input entered
            window['-OUTPUT-'].update('Please select a category first')
        elif category_input in budget_dict.keys():
            amount = budget_dict[category_input][0]['total']
            # ensure the amount is float type
            if type(amount) != 'float':
                amount = float(amount)
            stored_ledger = budget_dict[category_input][1:]
            record_item = category(category_input, amount)
            window['-OUTPUT-'].update(f"Category {values['-CATEGORY-']}: current balance is ${amount:.2f}")
        else:
            amount = 0
            stored_ledger = []
            category_input = category_input.strip()
            category_input = category_input.lower()
            record_item = category(category_input, amount)
            window['-OUTPUT-'].update(f"Category {values['-CATEGORY-']}: current balance is ${amount:.2f}")

    # deposit
    elif event == '-DCONFIRM-':
        if 'category_input' not in locals():
            window['-OUTPUT-'].update('Please select or create a category first')
        elif not values['-DAMOUNT-'].isnumeric():
            window['-OUTPUT-'].update('Please enter numbers for amount.', text_color = 'red')
        else:
            amount = values['-DAMOUNT-']
            description = values['-DDESCRIPTION-']
            amount = float(amount)
            record_item.deposit(amount, description)
            window['-OUTPUT-'].update(f"${amount:.2f} deposited to {record_item.category}")

    # withdraw
    elif event == '-WCONFIRM-':
        if 'category_input' not in locals():
            window['-OUTPUT-'].update('Please select or create a category first')
        elif not values['-WAMOUNT-'].isnumeric():
            window['-OUTPUT-'].update('Please enter numbers for amount.')
        else:
            amount = values['-WAMOUNT-']
            description = values['-WDESCRIPTION-']
            amount = float(amount)
            record_item.withdraw(amount, description)
            if record_item.indicator is False:
                window['-OUTPUT-'].update(f"Withdraw failed. {record_item.category}'s current balance is ${record_item.ledger[0]['total']:.2f}",
                                          text_color = 'red')
            elif record_item.indicator is True:
                window['-OUTPUT-'].update(f"${amount:.2f} withdrawn from {record_item.category}")

    # transfer
    elif event == '-TCONFIRM-':
        if 'category_input' not in locals():
            window['-OUTPUT-'].update('Please select or create a category first')
        elif not values['-TAMOUNT-'].isnumeric():
            window['-OUTPUT-'].update('Please enter numbers for amount.', text_color = 'red')
        else:
            amount = values['-TAMOUNT-']
            transfer_category = values['-TDESCRIPTION-']
            amount = float(amount)
            # create transfer object
            transfer_item_amount = budget_dict[transfer_category][0]['total']
            transfer_stored_ledger = budget_dict[transfer_category][1:]
            transfer_item = category(transfer_category, transfer_item_amount)
            record_item.transfer(amount, transfer_item)
            if record_item.indicator is False:
                window['-OUTPUT-'].update(f"Transfer failed. {transfer_item.category}'s current balance is ${transfer_item_amount:.2f}",
                                          text_color = 'red')
            elif record_item.indicator is True:
                # transfer is successful. Update the transfer item ledger
                transfer_item.ledger = transfer_item.ledger + transfer_stored_ledger
                budget_dict[transfer_item.category] = transfer_item.ledger
                window['-OUTPUT-'].update(f"${amount:.2f} transferred {record_item.category}")

    # show statement
    elif event == '-SHOW-':
        if 'category_input' not in locals():
            window['-OUTPUT-'].update('Please select or create a category first')
        else:
            statement()

    elif event == '-SAVE-':
        if 'category_input' not in locals():
            window['-OUTPUT-'].update('Please select or create a category first')
        else:
            record_item.ledger = record_item.ledger + stored_ledger
            budget_dict[record_item.category] = record_item.ledger
            with open(file_path, 'w') as file_handle:
                json.dump(budget_dict, file_handle)

window.close()