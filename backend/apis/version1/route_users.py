from fastapi import APIRouter
from sqlalchemy.orm import session
from fastapi import Depends

from schemas.users import UserCreate, ShowUser
from db.session import get_db
from db.repository.users import create_new_user

router = APIRouter()

@router.post("/", response_model = ShowUser)
def create_user(user: UserCreate,db: session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user