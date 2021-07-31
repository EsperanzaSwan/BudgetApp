# Budget App - Developed Using PySimpleGUI

This app tracks the deposit and spending in categories set by the user. It is developed with Python 3.8 and 
PySimpleGUI 4.45.0. 

## Run the app

Download the file and run the app using the following command:

``` bash
git clone https://github.com/EsperanzaSwan/BudgetApp.git
cd BudgetApp 
python3 record_SimpleGUI.py
```
If you receive an error message `No module named 'PySimpleGUI'`, you can install PySimpleGUI:

``` bash
pip3 install --user PySimpleGUI
```
User Interface

<img src = https://github.com/EsperanzaSwan/BudgetApp/blob/master/App_GUI.png>

Choose a category then deposit, withraw or transfer funds from another category. Please click **Confirm** every time after performing an action. 

Once you are done, click **Save Changes** to save the previous actions. You can click **Statement** to show the statment for the selected category. 

<img src = https://github.com/EsperanzaSwan/BudgetApp/blob/master/Statement.png>
