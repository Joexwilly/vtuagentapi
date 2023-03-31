from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, nullable = False, unique = True, index = True)
    hashed_password = Column(String, nullable = False)
    wallet = Column(BigInteger, default=0)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    jobs = relationship("Job", back_populates="owner")
    transactions = relationship("Transaction", back_populates="owner")