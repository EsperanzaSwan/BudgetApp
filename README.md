# Budget App - Developed Using PySimpleGUI

This app tracks the deposit and spending in categories set by the user. It is developed with Python 3.8 and 
PySimpleGUI 4.45.0. 

## Installation
```bash
git clone git@github.com:EsperanzaSwan/BudgetApp.git

# default name when no other is given
cd <BudgetApp>

poetry install
```

Alternative you can use any other virtual environment e.g. pythons `venv`:

```bash
git clone git@github.com:EsperanzaSwan/BudgetApp.git

# default name when no other is given
cd <BudgetApp>

# use .venv or any name you want
python3 -m venv .venv # python -m venv .venv on a Windows machine

source ./.venv/bin/activate #  .\.venv\Scripts\activate on a Windows machine

pip3 install -r ./requirements.txt # pip install -r .\requirements.txt on a Windows machine
```
## How to Use the App

Run the app using the following command:

``` bash
python3 record_SimpleGUI.py
```
If you receive an error message `No module named 'PySimpleGUI'`, you can install PySimpleGUI:

``` bash
pip install --user PySimpleGUI
```
The User Interface

