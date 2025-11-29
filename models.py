'''
APM:
dar class transaction niazi b default baraye sootone type nist.
hamchnin yadeton bashe bekahhdi default bezarid fght miseh yek value gozasht na do value
hamchjnin az qutation bayad estefade shavad yani 'deposit' doroste, na deposit

moafagh bashid
'''
# '''
# Class --> vasl bshe b sootone databaset
#
# '''
#
#
# from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from database import Base
#
#
#
# #--------------------TABLE K MIKHAY BSAZI CLASS------
#
#
# #_----costumer table------
# ''''
#
# ------customers---------------
# id name      email       password   card_number      accounts
# 1   ali    ali@gmail.com   123456    23282717231       accoutn(details....)
# 2   reza   reza@gmail.com  123456                   [4,5]
#
#
# ---account------
# id balance type pin ..   card_number
#
# '''
from datetime import datetime


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name= Column(String, nullable=False)
    email= Column(String, unique=True)
    password=Column(Integer,nullable=False)
    age=Column(Integer,nullable=True)
    phone=Column(Integer,nullable=False)
    address=Column(String,nullable=False)

    accounts= relationship("Account", back_populates="customers")
    transactions=relationship("Transaction", back_populates="customers")




#-------Accounts------
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    balance= Column(Float, default=0.0) #mojodi , 00
    type = Column(String, default="standard") # 'standard', 'foreign', 'crypto'
    pin = Column(String, nullable=False) #pin kodom account ro khod kon
    customer_id= Column(Integer, ForeignKey("customers.id"))
    card_number=Column(String,nullable=False)
    
    #-------relationships-----
    customers= relationship("Customer", back_populates="accounts")
    transactions= relationship("Transaction", back_populates="accounts")



#-------Transactions------
class Transaction(Base):
    __tablename__="transactions"
    id=Column(integre,primary_key=True)
    amount=Column(Float,nullable=False)
    from_account_id=Column(Integer,Forigenkey("accounts.id"))
    to_account_id=Column(Integer,Forigenkey("accounts.id"))
    type=Column(String,nullable=False)
    times=Column(DateTime,defult=datetime.utcnow)

    accounts=releationship("Account",back_populates=transactions)
    customers=relationship("Customer", back_populates=transactions)



