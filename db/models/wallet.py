from datetime import date
from sqlalchemy import DECIMAL, Column, Double, Integer, String, Boolean, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.repository.datetime import formatted_datetime


from db.base_class import Base

# wallet balance model
# class Wallet(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     #decimal balance type with 2 decimal places
#     balance = Column(DECIMAL(10, 2), default=0.00)
#     # relationship
#     user = relationship('User', back_populates='wallet', cascade="all, delete")
#     #back populate wallet history
#     wallethistory = relationship('WalletHistory', back_populates='wallet', cascade="all, delete")


# #wallet balance History contains balance before, after, amount added or subtracted, date and time
# class WalletHistory(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     wallet_id = Column(Integer, ForeignKey('wallet.id'))
#     user_id = Column(Integer, ForeignKey('user.id'))
#     balance_before = Column(DECIMAL(10, 2), default=0.00)
#     balance_after = Column(DECIMAL(10, 2), default=0.00)
#     amount = Column(DECIMAL(10, 2), default=0.00)
#     #create reference field, if empty, generate a random string
#     reference = Column(String, nullable = True, unique = True)
#     date_time = Column(DateTime, default=formatted_datetime)

#     # relationship
#     wallet = relationship('Wallet', back_populates='wallethistory')
#     user = relationship('User', back_populates='wallethistory')


class Wallet(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    balance = Column(DECIMAL(10, 2), default=0.00)
    user = relationship('User', back_populates='wallet', cascade="all, delete")
    wallethistory = relationship('WalletHistory', back_populates='wallet', cascade="all, delete")


class WalletHistory(Base):
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey('wallet.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    balance_before = Column(DECIMAL(10, 2), default=0.00)
    balance_after = Column(DECIMAL(10, 2), default=0.00)
    amount = Column(DECIMAL(10, 2), default=0.00)
    reference = Column(String, nullable=True, unique=True)
    date_time = Column(DateTime, default=formatted_datetime)
    wallet = relationship('Wallet', back_populates='wallethistory', cascade="all, delete")
    user = relationship('User', back_populates='wallethistory', cascade="all, delete")


