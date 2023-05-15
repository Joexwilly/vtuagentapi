#containing page names, their discounts in percentage and whether they are active or not
from sqlalchemy.orm import Session
from schemas.page_discounts import PageDiscountBase
from db.models.page_discounts import PageDiscount


#add new page discount
def create_new_page_discount(page_discount: PageDiscountBase,db: Session):
    page_discount_object = PageDiscount(**page_discount.dict())
    db.add(page_discount_object)
    db.commit()
    db.refresh(page_discount_object)
    return page_discount_object

# get page discount by page name
def retreive_page_discount(page_name:str,db:Session):
    item = db.query(PageDiscount).filter(PageDiscount.page_name == page_name).first()
    return item

# list all page discounts in the database
def list_page_discounts(db:Session):
    page_discounts = db.query(PageDiscount).all()
    return page_discounts

# delete page discount by page name
def delete_page_discount_by_page_name(page_name: str,db: Session):
    existing_page_discount = db.query(PageDiscount).filter(PageDiscount.page_name == page_name)
    if not existing_page_discount.first():
        return 0
    existing_page_discount.delete(synchronize_session=False)
    db.commit()
    return 1

# update page discount by page name
def update_page_discount_by_page_name(page_name:str, page_discount: PageDiscountBase,db: Session):
    existing_page_discount = db.query(PageDiscount).filter(PageDiscount.page_name == page_name)
    if not existing_page_discount.first():
        return 0
    existing_page_discount.update(page_discount.__dict__)
    db.commit()
    return 1

