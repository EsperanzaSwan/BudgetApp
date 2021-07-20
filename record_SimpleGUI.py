import PySimpleGUI as sg
import json
from budget import category


def statement():
    layout = [[sg.Text("New Window", key="new")]]
    window = sg.Window('Statement', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()


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
           sg.Combo(values=category_list, size=(15, 3), font=('calibri', 15), key='-CATEGORY-'),
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
           sg.Text('Category', font=('calibri', 15, 'bold'), size = (18,1)),
           sg.Input(font=('calibri', 15), key='-TDESCRIPTION-', size=(20, 1)),
           sg.Button(button_text='Confirm', font=('calibri', 13, 'bold'), key='-TCONFIRM-')],
          [sg.Button('Show Statement', pad=((280, 0), (15, 10)), font=('calibri', 13, 'bold'), key ='-SHOW-')],
          [sg.Button('Exit', pad=((320, 0), (15, 10)), font=('calibri', 13, 'bold'))]]
window = sg.Window('Budget App', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
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
            window['-OUTPUT-'].update('Category ' + values['-CATEGORY-'] + ': current balance is $' + str(amount))
        else:
            amount = 0
            stored_ledger = []
            category_input = category_input.strip()
            category_input = category_input.lower()
            record_item = category(category_input, amount)
            window['-OUTPUT-'].update('Category ' + values['-CATEGORY-'] + ': current balance is $' + str(amount))

    # deposit
    elif event == '-DCONFIRM-':
        if 'record_item' not in locals():
            window['-OUTPUT-'].update('Please select a category first')
        elif not values['-DAMOUNT-'].isnumeric():
            window['-OUTPUT-'].update('Please enter numbers for amount.', text_color = 'red')
        else:
            amount = values['-DAMOUNT-']
            description = values['-DDESCRIPTION-']
            amount = float(amount)
            record_item.deposit(amount, description)
            window['-OUTPUT-'].update('$' + str(amount) + ' deposited to ' + record_item.category)
    # withdraw
    elif event == '-WCONFIRM-':
        if 'record_item' not in locals():
            window['-OUTPUT-'].update('Please select a category first')
        elif not values['-WAMOUNT-'].isnumeric():
            window['-OUTPUT-'].update('Please enter numbers for amount.')
        else:
            amount = values['-WAMOUNT-']
            description = values['-WDESCRIPTION-']
            amount = float(amount)
            record_item.withdraw(amount, description)
            if record_item.indicator is False:
                window['-OUTPUT-'].update('Withdraw failed. ' + record_item.category + 'current balance is $' + str(record_item.ledger[0]['total']),
                                          text_color = 'red')
            if record_item.indicator is True:
                window['-OUTPUT-'].update('$' + str(amount) + ' withdrawn from ' + record_item.category)

    # transfer
    elif event == '-TCONFIRM-':
        if 'record_item' not in locals():
            window['-OUTPUT-'].update('Please select a category first')
        else:
            amount = values['-DAMOUNT-']
            description = values['-DDESCRIPTION-']
    # show statement
    elif event == '-SHOW-':
        if 'category_input' not in locals():
            window['-OUTPUT-'].update('Please select a category first')
        else:
            statement()

window.close()