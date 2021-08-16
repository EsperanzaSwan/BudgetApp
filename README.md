# Budget App - Developed Using PySimpleGUI

This app tracks the deposit and spending in categories set by the user. It is developed with Python 3.8 and 
PySimpleGUI 4.45.0. The project contains four files. `Budget.py` defines class `category` and methods such as
deposit, withdraw and transfer. `record_SimpleGUI.py` defines the user interface. `test_budget.py` is the unit test module.
`Ledger.json` stores all the data. 

## Installation

Download the file and run the app using the following command:

``` bash
git clone https://github.com/M-Theresa/BudgetApp.git
# default folder name if no other name is given
cd BudgetApp 
poetry install
python3 record_SimpleGUI.py
```

## Use the app

User Interface

<img src = https://github.com/M-Theresa/BudgetApp/blob/59c41a40d113d7cbe89a7a17dcc60a4deeeaff02/app_GUI.png>

Choose a category then deposit, withraw or transfer funds from another category. Please click **Confirm** every time after performing an action. 

You can click **Show Statement** to show the statement for the selected category. When you are done, click **Exit** to quit.
When exiting, the app saves all the data to a json file `ledger.json`.

<img src = https://github.com/M-Theresa/BudgetApp/blob/59c41a40d113d7cbe89a7a17dcc60a4deeeaff02/Statement.png>
