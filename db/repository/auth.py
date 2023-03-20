#db >repository > login.py
from sqlalchemy import or_
from sqlalchemy.orm import Session

from db.models.users import User 


# def get_user(phone:str,db: Session):
#     user = db.query(User).filter(User.phone || User.email == phone).first()
#     return user
#UPDATED: user can login with phone or email
def get_user(phone: str, db: Session):
    user = db.query(User).filter(or_(User.phone == phone, User.email == phone)).first()
    return user


def get_user_by_email(email: User.email,  db:Session):             #new
    user = db.query(User).filter(User.email == email).first()
    return user