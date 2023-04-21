from typing import Optional
from pydantic import BaseModel, condecimal
from datetime import date,datetime

#transaction schema

class TransactionBase(BaseModel):
    amount : int
    reference : str
    status : Optional[str] = None
    memo : Optional[str] = None
    extras : Optional[str] = None
    transaction_type : Optional[str] = None
    transaction_date : datetime = datetime.now()
    balance_before :  condecimal(max_digits=10, decimal_places=2)
    balance_after :  condecimal(max_digits=10, decimal_places=2)
    is_active : bool = True

class ShowTransaction(TransactionBase):
    amount : int
    reference : str
    status : str
    memo : str
    extras : str
    transaction_type : str
    transaction_date : datetime
    balance_before :  condecimal(max_digits=10, decimal_places=2)
    balance_after :  condecimal(max_digits=10, decimal_places=2)
    is_active : bool 
    
        
    class Config():  #to convert non dict obj to json
        orm_mode = True