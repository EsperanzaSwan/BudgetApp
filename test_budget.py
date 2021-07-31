"""
This test module tests module budget.py

"""

import unittest
from budget import category
from datetime import date

class test_budget(unittest.TestCase):

    # test initialization
    def test_initialization(self):
        test_object_A = category('Food', 500)
        expected_category = 'Food'
        expected_ledger = [{'total': 500}]
        self.assertEqual(test_object_A.category, expected_category, 'The category was not created correctly')
        self.assertEqual(test_object_A.ledger, expected_ledger, 'The ledger was not created correctly')

    # test deposit with description
    def test_desposit(self):
        opening_balance = 500
        test_object_A = category('Food', opening_balance)
        description = 'Extra Cash'
        deposit_amount = 500
        test_object_A.deposit(deposit_amount, description)
        actual_amount = opening_balance + deposit_amount
        actual_ledger = [{'total': actual_amount}, {'amount': deposit_amount, 'description': description, 'date': str(date.today())}]
        self.assertEqual(test_object_A.ledger[0], actual_ledger[0], "the total didn't update correctly")
        self.assertEqual(test_object_A.ledger[1:], actual_ledger[1:], "the ledger record didn't update correctly")

    # test deposit without description
    def test_desposit_no_description(self):
        opening_balance = 500
        test_object_A = category('Food', opening_balance)
        description = ''
        deposit_amount = 500
        test_object_A.deposit(deposit_amount, description)
        actual_amount = opening_balance + deposit_amount
        actual_ledger = [{'total': actual_amount},
                         {'amount': deposit_amount, 'description': description, 'date': str(date.today())}]
        self.assertEqual(test_object_A.ledger[0], actual_ledger[0], "the total didn't update correctly")
        self.assertEqual(test_object_A.ledger[1:], actual_ledger[1:], "the ledger record didn't update correctly")

    # test check funds
    def test_check_funds(self):
        test_object = category('Food', 500)
        self.assertTrue(test_object.check_funds(400), "The function didn't return true")
        self.assertFalse(test_object.check_funds(600), "The function didn't return false")

    # test withdraw successful
    def test_withdraw_success(self):
        opening_balance = 500
        test_object_A = category('Food', opening_balance)
        description = 'Buy food'
        withdraw_amount = 300
        test_object_A.withdraw(withdraw_amount, description)
        actual_amount = opening_balance - withdraw_amount
        actual_ledger = [{'total': actual_amount},
                         {'amount': -withdraw_amount, 'description': description, 'date': str(date.today())}]
        self.assertEqual(test_object_A.ledger[0], actual_ledger[0], "the total didn't update correctly")
        self.assertEqual(test_object_A.ledger[1:], actual_ledger[1:], "the ledger record didn't update correctly")

    # test withdraw failed
    def test_withdraw_fail(self):
        opening_balance = 400
        test_object_A = category('Food', opening_balance)
        description = 'Buy food'
        withdraw_amount = 600
        actual_ledger = [{'total': opening_balance}]
        test_object_A.withdraw(withdraw_amount, description)
        self.assertFalse(test_object_A.indicator, "the indicator is not set to false")
        self.assertEqual(test_object_A.ledger[0], actual_ledger[0], "the total didn't update correctly")
        self.assertEqual(test_object_A.ledger[1:], actual_ledger[1:], "the ledger record didn't update correctly")

    # test transfer successful
    def test_transfer_success(self):
        object_A_amount = 400
        test_object_A = category('Food', object_A_amount)
        object_B_amount = 700
        test_object_B = category('Entertainment', object_B_amount)
        transfer_amount = 100
        transfer_from_ledger = [{'total': object_B_amount - transfer_amount},
                                {'amount': -transfer_amount, 'description': 'Transfer to Food', 'date': str(date.today())}]
        transfer_to_ledger = [{'total': object_A_amount + transfer_amount},
                                {'amount': transfer_amount, 'description': 'Transfer from Entertainment', 'date': str(date.today())}]
        test_object_A.transfer(transfer_amount, test_object_B)
        self.assertTrue(test_object_A.indicator, "the indicator is not set to True")
        self.assertEqual(test_object_A.ledger[0], transfer_to_ledger[0], "the total of transferee didn't update correctly")
        self.assertEqual(test_object_B.ledger[0], transfer_from_ledger[0], "the total of transferor didn't update correctly")
        self.assertEqual(test_object_A.ledger[1:], transfer_to_ledger[1:], "the transferee's ledger record didn't update correctly")
        self.assertEqual(test_object_B.ledger[1:], transfer_from_ledger[1:], "the transferor's ledger record didn't update correctly")

    # test transfer failed
    def test_transfer_fail(self):
        object_A_amount = 400
        test_object_A = category('Food', object_A_amount)
        object_B_amount = 700
        test_object_B = category('Entertainment', object_B_amount)
        transfer_amount = 800
        transfer_from_ledger = [{'total': object_B_amount}]
        transfer_to_ledger = [{'total': object_A_amount}]
        test_object_A.transfer(transfer_amount, test_object_B)
        self.assertFalse(test_object_A.indicator, "the indicator is not set to false")
        self.assertEqual(test_object_A.ledger[0], transfer_to_ledger[0], "the total of transferee didn't update correctly")
        self.assertEqual(test_object_B.ledger[0], transfer_from_ledger[0], "the total of transferor didn't update correctly")
        self.assertEqual(test_object_A.ledger[1:], transfer_to_ledger[1:], "the transferee's ledger record didn't update correctly")
        self.assertEqual(test_object_B.ledger[1:], transfer_from_ledger[1:], "the transferor's ledger record didn't update correctly")

    def test_get_balance(self):
        test_object = category('Food', 500)
        expected = 'Current Balance is 500'
        self.assertEqual(test_object.get_balance(), expected, 'The balance statement is incorrect')

if __name__ == '__main__':
    unittest.main()