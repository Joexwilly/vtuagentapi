from typing import Optional
from pydantic import BaseModel
from datetime import date,datetime

#transaction schema

class TransactionBase(BaseModel):
    amount : int
    reference : str
    status : Optional[str] = None
    memo : Optional[str] = None
    transaction_type : Optional[str] = None
    transaction_date : date = datetime.now().date()
    is_active : bool = True

class ShowTransaction(TransactionBase):
    amount : int
    reference : str
    status : str
    memo : str
    transaction_type : str
    transaction_date : date
    is_active : bool 
    
        
    class Config():  #to convert non dict obj to json
        orm_mode = True