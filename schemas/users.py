from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, EmailStr, condecimal, constr
from db.models.users import User
from db.models.wallet import Wallet
from schemas.jobs import ShowJob

from schemas.wallet import ShowWallet, WalletBase

#properties required during user creation
class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    #gender: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_superuser: bool
      
    
    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True
 

class ShowUser(BaseModel): 
    id: int  
    name: str
    phone : str 
    email : EmailStr
    is_active : bool
    wallet: list[ShowWallet]
    #job: list[ShowJob]

  # add show walllet model balance
    #user_id: int
 
    

  
  


    #gender: str
    

    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True




 