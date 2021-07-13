''''

This test module tests module budget.py

'''

import unittest
from budget import category
from datetime import date

class test_budget(unittest.TestCase):

    def test_initialization(self):
        test_object_A = category('Food', 500)
        expected_category = 'Food'
        expected_ledger = [{'total': 500}]
        self.assertEqual(test_object_A.category, expected_category, 'The category was not created correctly')
        self.assertEqual(test_object_A.ledger, expected_ledger, 'The ledger was not created correctly')

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

    def test_withdraw_success(self):
        opening_balance = 500
        test_object_A = category('Food', opening_balance)
        description = 'Buy food'
        withdraw_amount = 300
        actual_amount = opening_balance - withdraw_amount
        actual_ledger = [{'total': actual_amount},
                         {'amount': -withdraw_amount, 'description': description, 'date': str(date.today())}]
        self.assertTrue(test_object_A.withdraw(withdraw_amount, description), "the function didn't return true")
        self.assertEqual(test_object_A.ledger[0], actual_ledger[0], "the total didn't update correctly")
        self.assertEqual(test_object_A.ledger[1:], actual_ledger[1:], "the ledger record didn't update correctly")

    def test_withdraw_fail(self):
        opening_balance = 400
        test_object_A = category('Food', opening_balance)
        description = 'Buy food'
        withdraw_amount = 600
        actual_ledger = [{'total': opening_balance}]
        self.assertFalse(test_object_A.withdraw(withdraw_amount, description), "the function didn't return false")
        self.assertEqual(test_object_A.ledger[0], actual_ledger[0], "the total didn't update correctly")
        self.assertEqual(test_object_A.ledger[1:], actual_ledger[1:], "the ledger record didn't update correctly")


if __name__ == '__main__':
    unittest.main()