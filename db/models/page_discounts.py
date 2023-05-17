from db.base_class import Base
from sqlalchemy import DECIMAL, Column, DateTime, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.repository.datetime import formatted_datetime

# #page discount having page enabled 
class PageDiscount(Base):
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, nullable = False)
    #page discount in percentage
    discount = Column(DECIMAL(10, 2), default=0.00, nullable = True)
    is_active = Column(Boolean(), default=True)
    date_created = Column(DateTime, default=formatted_datetime)
 