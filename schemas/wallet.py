from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, condecimal
from datetime import date,datetime

# wallet schema
class WalletBase(BaseModel):
    user_id: Optional[int] = None
  #user_id is id of the user who owns the wallet

    balance: Optional[condecimal(max_digits=10, decimal_places=2)] = None



class ShowWallet(WalletBase):
    user_id: int
    balance: condecimal(max_digits=10, decimal_places=2)

    class Config():
        orm_mode = True


class WalletCreate(BaseModel):
   
    # balance field that cannot be changed from 0.00
    balance: condecimal(max_digits=10, decimal_places=2) = 0.00
    class Config():
        orm_mode = True


#update wallet balance by selecting add or subtract boolean
class UpdateWalletBalance(BaseModel):

    balance: condecimal(max_digits=10, decimal_places=2)


    class Config():
        orm_mode = True



  