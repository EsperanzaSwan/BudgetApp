class Category():
    # initialize the object
    def __init__(self, eachCategory, balance = 0):
        self.category = eachCategory
        self.ledger = [{'total': balance}]

    def deposit(self, amount, description = ''):
        self.ledger.append({'amount': amount, 'description': description})
        self.ledger[0]['total'] = self.ledger[0]['total'] + amount

    # check if there is enough funds on the account
    def check_funds(self, amount):
        if self.ledger[0]['total'] < amount:
            return False
        else:
            return True

    def withdraw(self, amount, description=''):
        # check if there is enought funds
        if self.check_funds(amount) is True:
            self.ledger.append({'amount': -amount, 'description': description})
            self.ledger[0]['total'] = self.ledger[0]['total'] - amount
            return True
        # return True if withdraw is successful. Return false if not
        else:
            return False

    def transfer(self, amount, anotherCategory):
        # check if there is enought funds
        if anotherCategory.check_funds(amount) is True:
            anotherCategory.withdraw(amount, f'Transfer to {self.category}')
            self.deposit(amount, f'Transfer from {anotherCategory.category}')
            return True
        # return True if withdraw is successful. Return false if not
        else:
            return False

    def get_balance(self, amount):
        print(f"Current Balance is {self.ledger[0]['total']}")

A = Category('food')
B = Category('Clothes', 500)
A.deposit(100, 'pay check')
A.transfer(200, B)
print(A.ledger)