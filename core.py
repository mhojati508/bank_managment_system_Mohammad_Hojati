#salam ostad vaght bekheir. kheli mamanon az nazarat arzeshmandetun. eslahati ke farmude budid anjam dadam be joz Note4
#ke motasefaneh koli fekr kardam vali natunestam be natijeh beresam. mamnoon misham bishtar rahnamii befrmaiid. 
'''
APM: Kheyli awli

Note 1 : 
    fght dar fucntion create_account , vaghty card number ro misaze bayad
    bere va tooye database begarde bebine in card number vojod nadashte bashe 
    age vojod dahst ( khob nemish ecard number tkrari dad pas jadid hads mizane)
    mishe az While estefade krd inja ( albate baraye porozhe niazi nist ama besoorate real world 
    eshare kardam)


Note 2 :
    Print ha bayad ghable return bashand agar bekhahid ejra beshanavd (man sahih krdm dar tabeye withdraw()

Note3 :
    hamchenin bad az elif dar tabeye withdraw() , yek else gozashtam ke age mojodi kafi nabod
    be moshtari bege k mojoodi nadari. hamin kar ra dar tavabeye digar piade konid (mesle transfer)

Note4:
    baraye tabeye show_transaction() , shoma bayad harjaee k deposit ya withdraw hast
    yek data varede tabel transaction konid k hame pardakhti ha o hamechi sabt beshe
    badesh avghty az show_transaction() estefade sho tamame record haye databse ro 
    neshoon bede



dar har koja az note ha agar moshkel ya soal dashtid haminja rahat beporsid
moafagh bashid


NOTE 4 --> bebinid dar tabeye deposit baratoon dorost krdm
vaghty kasi deposit kard in deposit amountesh kamel dar tabel transaction sabt mishe
shoma bayad hamchin chizi ro baraye whitdraw va transfer ham bzarid 
k user harkari k kard , yani pool keshid , pol variz krd ya harchi haamsh sabt she
vaghty k tabeye show_transaction ro bekhad negah kone , in tabe bayad tamame dade haye oon user ro print kon

'''

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
      
        elif amount < account.balance:
            account.balance = account.balance - amount
            self.session.commit()
            print(f"your account balance is: {account.balance}")
            return account
    
        else:
            print('your balance is not enough for withdraw')
            return None
    

    def transfer(self, from_account_id: int, to_account_id: int, amount: float)-> tuple[Account, Account, Account]:
        from_account = self.session.get(Account, from_account_id)
        
        if not from_account:
            print(f'account {from_account_id} not found')
            raise Exception(f'Account with id {from_account_id} not found')
        to_account= self.session.get(Account, to_account_id)
        if not to_account:
            print(f'To-account {to_account_id} not found')
            raise Exception(f'Account with id {to_account_id} not found')
        
        if from_account_id == to_account_id:
            raise ValueError("Cannot transfer to the same account")
        
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        
        elif  amount < from_account.balance:
            from_account.balance -= amount
            to_account.balance += amount
            self.session.commit()
            return f'withdraw from {from_account_id}, deposit to {to_account_id}, amount {amount} '
        
        else:
            print('your balance is not enough for transfer')
            return None
        

    # '''
    #     account from --> pull balance+ --> farde dg
    # '''



    def show_transaction(self, account_id: int)-> list[Account]:
        account = self.session.get(Account, account_id)
        if not account:
            print(f'account {account_id} not found')
            raise Exception(f'Account with id {account_id} not found')
