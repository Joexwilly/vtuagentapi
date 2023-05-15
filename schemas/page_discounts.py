from typing import Optional
from pydantic import BaseModel, condecimal
from datetime import date,datetime

#page names and their discounts in percentage and whether they are active or not

class PageDiscountBase(BaseModel):
    page_name : str
    discount :  condecimal(max_digits=10, decimal_places=2)
    is_active : bool = True

class ShowPageDiscount(PageDiscountBase):
    page_name : str
    discount :  condecimal(max_digits=10, decimal_places=2)
    is_active : bool 
    
    
    class Config():  #to convert non dict obj to json
        orm_mode = True