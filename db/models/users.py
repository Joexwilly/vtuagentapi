from sqlalchemy import Column, DateTime, Integer, Numeric, String, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from db.repository.datetime import formatted_datetime

from db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, nullable = False, unique = True, index = True)
    hashed_password = Column(String, nullable = False)
    is_active = Column(Boolean(), default=True)
    #add balance field with decimal type
    balance = Column(Numeric(precision=10, scale=2), default=0.00)

    is_superuser = Column(Boolean(), default=False)
    is_logged_in = Column(Boolean(), default=False)
    #date created
    date_created = Column(DateTime, default=formatted_datetime)
    jobs = relationship("Job", back_populates="owner")
    transactions = relationship("Transaction", back_populates="owner", cascade="all, delete")
    wallet = relationship("Wallet", back_populates="user",cascade="all, delete")
    #back populate wallet history
    wallethistory = relationship("WalletHistory", back_populates="user", cascade="all, delete")
