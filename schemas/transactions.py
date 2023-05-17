from typing import Optional
from pydantic import BaseModel, condecimal
from datetime import date,datetime

#transaction schema

class TransactionBase(BaseModel):
    amount : condecimal(max_digits=10, decimal_places=2)
    reference : str
    status : Optional[str] = None
    memo : Optional[str] = None
    extras : Optional[str] = None
    transaction_type : Optional[str] = None
    transaction_date : datetime = datetime.now()
    balance_before :  condecimal(max_digits=10, decimal_places=2)
    balance_after :  condecimal(max_digits=10, decimal_places=2)
    

    
    

class ShowTransaction(TransactionBase):
    amount : condecimal(max_digits=10, decimal_places=2)
    reference : str
    status : str = None
    memo : str = None
    extras : str = None
    transaction_type : str = None
    transaction_date : datetime
    balance_before :  condecimal(max_digits=10, decimal_places=2)
    balance_after :  condecimal(max_digits=10, decimal_places=2)
    
    
        
    class Config():  #to convert non dict obj to json
        orm_mode = True