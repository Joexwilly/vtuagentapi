from typing import Optional
from pydantic import BaseModel, EmailStr, constr

#properties required during user creation
class UserCreate(BaseModel):
    phone: str
    email: EmailStr
    #gender: str
    password: str

class UserUpdate(BaseModel):
    phone: str
    email: EmailStr
      
    
    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True
 

class ShowUser(BaseModel): 
    id: int  
    phone : str 
    email : EmailStr
    #gender: str
    is_active : bool

    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True



 