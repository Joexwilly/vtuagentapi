from sqlalchemy.orm import Session
from schemas.users import UserCreate, ShowUser, UserUpdate
from db.models.users import User
from core.hashing import Hasher

#function to create new user, add to database,commit the changes and refresh the instance 
# to get the new generated Id
def create_new_user(user: UserCreate, db: Session):
    user = User(phone=user.phone, email=user.email, hashed_password= Hasher.get_password_hash(user.password),
    is_active=True, is_superuser=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#returns the first email address match in the database
# def get_user_by_email(email:str,db:Session):             
#     user = db.query(User).filter(User.email == email).first()
#     return user

def get_user_by_email(email: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user

# get user by id
def get_user_by_id(id:int,db:Session):
    user = db.query(User).filter(User.id == id).first()
    return user

#  get user by phone
def get_user_by_phone(phone:str,db:Session):
    user = db.query(User).filter(User.phone == phone).first()
    return user

# list all users in the database
def list_users(db:Session):
    jobs = db.query(User).all()
    return jobs

#delete user by id
def delete_user_by_id(id: int,db: Session):
    existing_user = db.query(User).filter(User.id == id)
    if not existing_user.first():
        return 0
    existing_user.delete(synchronize_session=False)
    db.commit()
    return 1

#update user by id
def update_user_by_id(id: int, user: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.id == id).first()
    if not existing_user:
        return 0
    existing_user.phone = user.phone
    existing_user.email = user.email
    existing_user.hashed_password = Hasher.get_password_hash(user.password)
    db.commit()
    return 1


