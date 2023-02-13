from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import session
from fastapi import Depends

from schemas.users import UserCreate, ShowUser
from db.session import get_db
from db.repository.users import create_new_user, get_user_by_id, get_user_by_email, list_users

router = APIRouter()

@router.post("/", response_model = ShowUser)
def create_user(user: UserCreate,db: session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user

# get user by id
@router.get("/{id}", response_model=ShowUser)
def get_user(id: int, db: session = Depends(get_db)):
    user = get_user_by_id(id=id, db=db)
    return user


# # list users route
@router.post("/all", response_model= List[ShowUser])
def get_users(db: session = Depends(get_db)):
    users = list_users(db=db)
    return users

# @router.get("/all",response_model=List[ShowJob]) 
# def read_jobs(db:Session = Depends(get_db)):
#     jobs = list_jobs(db=db)
#     return jobs