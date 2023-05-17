from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from db.session import get_db
from db.repository.page_discounts import create_new_page_discount,retreive_page_discount,list_page_discounts, update_page_discount_by_service_name,delete_page_discount_by_service_name
from typing import List
from schemas.page_discounts import PageDiscountBase, ShowPageDiscount
from api.version1.route_auth import get_current_user_from_token


router = APIRouter()

#page discounts routes

#create new page discount, only if user is superuser
@router.post("/create-page-discount/", response_model=ShowPageDiscount)
def create_page_discount(page_discount: PageDiscountBase, db: Session = Depends(get_db),current_user=Depends(get_current_user_from_token)):  #new dependency here
    if current_user.is_superuser == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to create page discounts")
    page_discount = create_new_page_discount(page_discount=page_discount, db=db)
    return page_discount


#get page discount by page name
@router.get("/get/{service_name}",response_model=ShowPageDiscount) # TAKE NOTEif we keep just "{id}" . it would stat catching all routes
def read_page_discount(service_name:str,db:Session = Depends(get_db)):
    page_discount = retreive_page_discount(service_name=service_name,db=db)
    if not page_discount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Page discount with this page name {service_name} does not exist")
    return page_discount

#get all page discounts
@router.get("/all",response_model=List[ShowPageDiscount])
def read_page_discounts(db:Session = Depends(get_db)):
    page_discounts = list_page_discounts(db=db)
    return page_discounts

#update page discount by page name
@router.put("/update/{service_name}")
def update_page_discount(service_name: str,page_discount: PageDiscountBase,db: Session = Depends(get_db),current_user=Depends(get_current_user_from_token)):
    if current_user.is_superuser == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update page discounts")
    message = update_page_discount_by_service_name(service_name=service_name,page_discount=page_discount,db=db)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Page discount with page name {service_name} not found")
    return {"msg":"Successfully updated data."}

#delete page discount by page name
@router.delete("/delete/{service_name}")
def delete_page_discount(service_name: str,db: Session = Depends(get_db),current_user=Depends(get_current_user_from_token)):
    if current_user.is_superuser == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete page discounts")
    page_discount = retreive_page_discount(service_name =service_name,db=db)
    if not page_discount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Page discount with page name {service_name} not found")
    message = delete_page_discount_by_service_name(service_name=service_name,db=db)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Page discount with page name {service_name} not found")
    return {"msg":"Successfully deleted."}






