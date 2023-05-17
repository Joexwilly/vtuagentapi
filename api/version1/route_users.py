from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.version1.route_auth import get_current_user_from_token
from core.hashing import Hasher
from fastapi.encoders import jsonable_encoder
import secrets
from email_config.send_email import send_registration_mail
from schemas.jobs import ShowJob
from schemas.users import UserCreate, ShowUser, UserUpdate
from db.session import get_db
from db.repository.users import create_new_user, get_user_by_id, get_user_by_email, get_user_id_by_email, list_users, get_user_by_phone, delete_user_by_id, update_user_by_id
from db.repository.wallet import create_new_wallet
from schemas.wallet import ShowWallet, WalletCreate
router = APIRouter()

#Here: I use read as a prefix to explain get, as in getting something from the database

@router.post("/", response_description="Register a user", response_model = ShowUser)
async def registration(user: UserCreate, db: Session = Depends(get_db)):
    #check for duplicate email
    email_found = get_user_by_email(email=user.email, db=db)
    phone_found = get_user_by_phone(phone=user.phone, db=db)
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    
    if phone_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone number already exists")



    user = create_new_user (user=user, db=db)

    #get user by id
    email_id = get_user_by_email(email=user.email, db=db)
    id = email_id.id
    
    #if user is found get the id and create a wallet for the user
    if user:
        create_new_wallet(wallet={ "balance": 0, }, db=db, user_id=id)




    #send registration email
   

    try:
        #send registration email
        await send_registration_mail("Registration Successful", user.email, {"title": "Registration Successful"})
    except Exception as e:
        # Log the error or take any other necessary action
        print(f"Failed to send registration email: {e}")

    return user


# #get user by email
@router.get("/email/{email}", response_model= ShowUser)
def read_user_email(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(email=email, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return user

# get user by id
@router.get("/{id}", response_model=ShowUser)
def read_user(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(id=id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# get user by phone
@router.get("/phone/{phone}", response_model= ShowUser)
def read_user_phone(phone: str, db: Session = Depends(get_db)):
    user = get_user_by_phone(phone=phone, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="Phone number not found")
    return user

# # list users route
@router.post("/all", response_model= #show ShowUser and ShowWallet
            List[ShowUser])
           # List[Union[ShowUser, ShowWallet]])
def get_users(db: Session = Depends(get_db)):
    
    users = list_users(db=db)
    return users


#delete user 
@router.delete("/delete/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(id=id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user_by_id(id=id,db=db)
    
    return "User deleted successfully"

#update user
@router.patch("/update/{id}")   
def update_user(id: int,user: UserUpdate, db: Session = Depends(get_db)):
    #current_user = 1
    message = update_user_by_id(id=id,user=user, db=db)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    return {"msg":"Successfully updated data."} 

#get current logged in user
@router.get("/me", response_model=ShowUser)
def read_users_me(current_user: ShowUser = Depends(get_current_user_from_token)):
    return current_user





