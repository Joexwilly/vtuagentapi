from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

#Transaction details model

class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable = False)
    reference = Column(String, nullable = False, unique = True)
    status = Column(String, nullable = True)
    memo = Column(String, nullable = True)
    transaction_type = Column(String, nullable = True)
    transaction_date = Column(Date)
    is_active = Column(Boolean(), default=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="transactions")