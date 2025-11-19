from database import get_session
from utils import hash_password, check_password
from models import Customer, Account, Transaction
import numpy as np
import random

class AdminPanel:
    def __init__(self):
        self.session = get_session()

    def card_number(self):
        digits = np.random.randint(0, 9, 16)
        card_number = "".join(map(str, digits))
        return card_number



    def create_customer(self, name, email, age, phone, address):
        # row tooye database besazam

        # ^^^
        # kare shomast *** age, phone, address tooye models.py inja ham bezarid *******
        customer = Customer(name=name, email=email, age=age, phone=phone, address=address)

        # ta alan classesho sakhti tooye python
        # zakhire bshe?? tooey db
        self.session.add(customer)
        self.session.commit()
        print(f'customer {name} created successfully')
        return customer

    def create_account(self, customer_id, account_type, balance, pin, card_number=None ):
        customer = self.session.get(Customer, customer_id)
        # row ro bekesham biron

        if not customer:
            # ^^^
            print(f'customer {customer_id} not found')
            raise Exception(f'Customer with id {customer_id} not found')

        # ^^^
        # card number shoam ezafe kon?????
        # numpy ---> gpt beporsid ???
        # card_number=328273817
        # def card_number(self):
        #     digits = np.random.randint(0, 9, 16)
        #     card_number = "".join(map(str, digits))
        #     return card_number

        # def card_number(self):
        #     return "".join(str(random.randit(0,9)) for _ in range(16))

        hashed_pin = hash_password(pin)
        if card_number is None:
            create_card_number=self.card_number()



        account = Account(balance=balance, type=account_type, pin=hashed_pin, card_number=create_card_number)
        self.session.add(account)
        self.session.commit()

        return account

    # -------

    def show_balance(self, account_id):
        account = self.session.get(Account, account_id)
        if not account:
            # ^^
            print(f'account {account_id} not found')
            raise Exception(f'Account with id {account_id} not found')

        balance = account.balance

        # ^^ print
        print(f'account balance: {balance}')
        return balance

    def deposit(self, account_id, amount):
        account = self.session.get(Account, account_id)
        if not account:
            # ^^
            print(f'account {account_id} not found')
            raise Exception(f'Account with id {account_id} not found')

        account.balance = account.balance + amount
        self.session.commit()
        return account

    def withdraw(self, account_id, amount):
        # ^^^^^^^^
        # '''
        # hatman check kone amount <balance
        # '''
        account = self.session.get(Account, account_id)
        if not account:
            print(f'account {account_id} not found')
            raise Exception(f'Account with id {account_id} not found')

        elif amount < account.balance:
            account.balance = account.balance - amount
            self.session.commit()
            return account
        #print()
        print(f"your account balance is: {account.balance}")


    def transfer(self, from_account_id, to_account_id, amount):
        from_account = self.session.get(Account, from_account_id)
        if not from_account:
            print(f'account {from_account_id} not found')
            raise Exception(f'Account with id {from_account_id} not found')
        to_account= self.session.get(Account, to_account_id)
        if not to_account:
            print(f'To-account {to_account_id} not found')
            raise Exception(f'Account with id {to_account_id} not found')
        if  amount < from_account.balance:
            from_account.balance -= amount
            to_account.balance += amount
            self.session.commit()
            return {'withdraw from': from_account_id, 'deposit to': to_account_id, 'amount': amount}

    # '''
    #     account from --> pull balance+ --> farde dg
    # '''



    def show_transaction(self, account_id):
        account = self.session.get(Account, account_id)
        if not account:
            print(f'account {account_id} not found')
            raise Exception(f'Account with id {account_id} not found')
        return account.balance
