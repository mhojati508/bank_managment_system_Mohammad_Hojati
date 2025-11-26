#salam ostad kheli mamnoonam az rhnami awli va kameli ke zahmat keshidid. cod ha ro kamel kardam ke khedmateton ersal mikonam.  

from database import get_session
from utils import hash_password, check_password
from models import Customer, Account, Transaction
import numpy as np
import random


class AdminPanel:
    def __init__(self):
        self.session = get_session()


    def create_customer(self, name: str, email: str, age: int, phone: str, address: str)-> Customer:
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

    def card_number(self):
        digits = np.random.randint(0, 9, 16)
        card_number = "".join(map(str, digits))
        return card_number
        """
        #way1
               def card_number(self):
                    digits = np.random.randint(0, 9, 16)
                    card_number = "".join(map(str, digits))
                    return card_number
               card_number = card_number()
               return card_number
         #way2      
         def card_number(self):
             return "".join(str(random.randit(0,9)) for _ in range(16))

        """

    def create_account(self, customer_id: int, account_type: str, balance: float, pin: str, card_number: str=None )-> Account:
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


        hashed_pin = hash_password(pin)

        if card_number is None:
            create_card_number=self.card_number()
                                                                            
        account = Account(balance=balance, type=account_type, pin=hashed_pin, card_number=create_card_number)
        self.session.add(account)
        self.session.commit()
        print(f"account {account_type} created successfully")
        return account

    # -------

    def show_balance(self, account_id: int)-> float:
        account = self.session.get(Account, account_id)

        # if not account:
        #     error_msg = f'Account with id {account_id} not found'
        #     print(error_msg)
        #     raise Exception(error_msg)
        if not account:
            # ^^
            print(f'account {account_id} not found')
            raise Exception(f'Account with id {account_id} not found')

        balance = account.balance

        # ^^ print
        print(f'account balance: {balance}')
        return balance

    def deposit(self, account_id: int, amount: float)-> Account:
        
        account = self.session.get(Account, account_id)
        if not account:
            # ^^
            print(f'account {account_id} not found')
            raise Exception(f'Account with id {account_id} not found')
        
        elif amount > 0:
            account.balance = account.balance + amount
            self.session.commit()

            #******* inja note 4 
            transaction = Transaction(amount=amount , from_account_id=account_id , to_account_id=account_id , type = 'deposition')
            self.session.add(transaction)
            self.session.commit()
            #-------
            
            return account
        else:
            raise ValueError("Deposit amount must be positive")
        

    def withdraw(self, account_id: int, amount: float)-> Account:
        # ^^^^^^^^
        # '''
        # hatman check kone amount <balance
        # '''
        
        account = self.session.get(Account, account_id)
        if not account:
            print(f'account {account_id} not found')
            raise Exception(f'Account with id {account_id} not found')
      
        if amount <=0:
            raise ValueError("withdraw amount must be positive")
        elif amount > account.balance: 
            raise ValueError("your balance is not enough for withdraw")
        else:
            account.balance = account.balance - amount
            self.session.add(account)
            self.session.commit()
            print(f"your account balance is: {account.balance}")

            transaction = Transaction(amount=amount , from_account_id=account_id , to_account_id=None , type = 'withdraw')
            self.session.add(transaction)
            self.session.commit()
            return account

    def transfer(self, from_account_id: int, to_account_id: int, amount: float) -> tuple[Account, Account]:
      from_account = self.session.get(Account, from_account_id)
      if not from_account:
        print(f'account {from_account_id} not found')
        raise Exception(f'Account with id {from_account_id} not found')

      to_account = self.session.get(Account, to_account_id)
      if not to_account:
        print(f'To-account {to_account_id} not found')
        raise Exception(f'Account with id {to_account_id} not found')
    
      if from_account_id == to_account_id:
        raise ValueError("Cannot transfer to the same account")
    
      if amount <= 0:
        raise ValueError("Transfer amount must be positive")
    
      if amount > from_account.balance:
        print("your balance is not enough")
        raise ValueError("Insufficient balance")
      if not from_account:
        print(f'account {from_account_id} not found')
        raise Exception(f'Account with id {from_account_id} not found')
      to_account = self.session.get(Account, to_account_id)
      if not to_account:
        print(f'To-account {to_account_id} not found')
        raise Exception(f'Account with id {to_account_id} not found')
    
      if from_account_id == to_account_id:
        raise ValueError("Cannot transfer to the same account")
    
      if amount <= 0:
        raise ValueError("Transfer amount must be positive")
    
      if amount > from_account.balance:
        print("your balance is not enough")
        raise ValueError("Insufficient balance")

      from_account.balance -= amount
      to_account.balance += amount
      self.session.commit()

      transaction = Transaction(amount=amount, from_account_id=from_account_id, to_account_id=to_account_id, type="transfer")
      self.session.add(transaction)
      self.session.commit()
      return from_account, to_account

    # '''
    #     account from --> pull balance+ --> farde dg
    # '''



    def show_transaction(self, account_id: int):
      transactions = self.session.query(Transaction).filter(Transaction.from_account_id == account_id or Transaction.to_account_id == account_id).all()
      if not transactions:
        print(f'No transactions found for account {account_id}')
        return
      for transaction in transactions:
        print(f'Transaction: {transaction.amount} from {transaction.from_account_id} to {transaction.to_account_id} on {transaction.timestamp}')
      return transactions
