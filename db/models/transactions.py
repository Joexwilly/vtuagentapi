from sqlalchemy import DECIMAL, Column, DateTime, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.repository.datetime import formatted_datetime

from db.base_class import Base

#Transaction details model

class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable = False)
    reference = Column(String, nullable = False, unique = True)
    status = Column(String, nullable = True)
    memo = Column(String, nullable = True)
    extras = Column(String, nullable = True)
    transaction_type = Column(String, nullable = True)
    transaction_date = Column(DateTime , default=formatted_datetime)
    balance_before = Column(DECIMAL(10, 2), default=0.00, nullable = True)
    balance_after = Column(DECIMAL(10, 2), default=0.00, nullable = True)
    is_active = Column(Boolean(), default=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="transactions", cascade="all, delete")