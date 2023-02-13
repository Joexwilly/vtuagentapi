from sqlalchemy.orm import Session
from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher

def create_new_user(user: UserCreate, db: Session):
    user = User(username=user.username, email=user.email, hashed_password= Hasher.get_password_hash(user.password),
    is_active=True, is_superuser=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(email:str,db:Session):             #new
    user = db.query(User).filter(User.email == email).first()
    return user

# list all users in the database
def list_users(db:Session):
    jobs = db.query(User).all()
    return jobs



# get user by id
def get_user_by_id(id:int,db:Session):
    user = db.query(User).filter(User.id == id).first()
    return user