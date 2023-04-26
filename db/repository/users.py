from sqlalchemy.orm import Session
from schemas.users import UserCreate, ShowUser, UserUpdate
from db.models.users import User
from db.models.wallet import Wallet
from core.hashing import Hasher
from sqlalchemy.orm import joinedload

from schemas.wallet import ShowWallet

#function to create new user, add to database,commit the changes and refresh the instance 
# to get the new generated Id
def create_new_user(user: UserCreate, db: Session):
    user = User(name= user.name, phone=user.phone, email=user.email, hashed_password= Hasher.get_password_hash(user.password),
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
    # list users showing Wallet database model fields 
#     users = db.query(User).join(Wallet).all()
#    # users = db.query(User).all()
#     return users
    # users = db.query(User).options(joinedload(User.wallet)).all()
    # return users
    users = db.query(User).options(joinedload(User.jobs),joinedload(User.wallet)
                                   ).all()
    # Extract fields from User and Wallet tables
    #show_users = [ShowUser(id=user.id, phone=user.phone, email = user.email, is_active = user.is_active, wallet=user.wallet) for user in users]
    #show_wallets = [ShowWallet(user_id=user.id, balance=wallet.balance) for user in users for wallet in user.wallet]
    # Combine show_users and show_wallets into a single list
    #all_data = show_users + show_wallets    



    #return all_data
    return users












    #return all_data




  



    #return user
    #show_users = [ShowUser(id=user.id, phone=user.phone, email = user.email, is_active = user.is_active, wallet=[ShowWallet(id=user.id, user_id=user.id,balance=wallet.balance) for wallet in user.wallet]) for user in users]
   # return show_users

#delete user by id
# def delete_user_by_id(id: int,db: Session):
#     existing_user = db.query(User).filter(User.id == id)
#     if not existing_user.first():
#         return 0
#     existing_user.delete(synchronize_session=False)
#     db.commit()
#     return 1

#delete user by id taking into account all the user relationships
def delete_user_by_id(id: int,db: Session):
    existing_user = db.query(User).filter(User.id == id).first()
    if not existing_user:
        return 0
    db.delete(existing_user)
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

#get wallet balance
def get_wallet_balance(id:int,db:Session):
    user = db.query(User).filter(User.id == id).first()
    return user.wallet

#get user id by email
def get_user_id_by_email(email:str,db:Session):
    user = db.query(User).filter(User.email == email).first()
    return user.id