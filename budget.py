from datetime import date

class category():
    # initialize the object
    def __init__(self, eachCategory, balance = 0):
        self.category = eachCategory
        self.ledger = [{'total': balance}]
        self.indicator = None

    # deposit the amount
    def deposit(self, amount, description = ''):
        self.ledger.insert(1, {'amount': amount, 'description': description, 'date': str(date.today())})
        self.ledger[0]['total'] = self.ledger[0]['total'] + amount

    # check if there is enough funds on the account
    def check_funds(self, amount):
        if self.ledger[0]['total'] < amount:
            return False
        else:
            return True

    # withdraw the money
    def withdraw(self, amount, description=''):
        # check if there is enought funds
        if self.check_funds(amount) is True:
            self.ledger.insert(1, {'amount': -amount, 'description': description, 'date': str(date.today())})
            self.ledger[0]['total'] = self.ledger[0]['total'] - amount
            self.indicator = True
        # set to true if withdraw is successful. set to false if not
        else:
            self.indicator = False

    # transfer funds
    def transfer(self, amount, anotherCategory):
        # check if there is enought funds
        if anotherCategory.check_funds(amount) is True:
            anotherCategory.withdraw(amount, f'Transfer to {self.category}')
            self.deposit(amount, f'Transfer from {anotherCategory.category}')
            self.indicator = True
        # set to True if transfer is successful. set to false if not
        else:
            self.indicator = False

    def get_balance(self):
        message = f"Current Balance is {self.ledger[0]['total']}"
        return message

