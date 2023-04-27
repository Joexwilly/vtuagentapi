from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import status,HTTPException
from jose import JWTError, jwt,ExpiredSignatureError
from db.models.users import User
from db.repository.auth import get_user, get_user_by_email, sms_otp, verify_sms_otp
import secrets
import base64
import json
from jose.jwt import ExpiredSignatureError


from db.session import get_db
from core.hashing import Hasher
from schemas.tokens import Token, TokenData, PasswordRequest
from email_config.send_email import password_reset

from core.security import create_access_token
from core.config import settings
from db.repository.users import get_user_by_id, get_user_by_phone
import secrets


router = APIRouter()

def authenticate_user(phone: str, password: str,db: Session):
    user = get_user(phone=phone ,db=db)
    
    
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    print(user.email, "just logged")
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session= Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone/email or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "expires_in": access_token_expires, "data":{"id": user.id, "name": user.name, "email": user.email, "phone": user.phone, "wallet": user.wallet, "is_active": user.is_active, "is_superuser": user.is_superuser}
            }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")  #new



#new function, It works as a dependency
def get_current_user_from_token(token: str = Depends(oauth2_scheme),db: Session=Depends(get_db)): 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        print("username/email extracted is ",email)
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email,db)
    if user is None:
        raise credentials_exception
    return user


def get_current_user_from_token_now(token: str,db: Session=Depends(get_db)): 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        print("username/email extracted is ",email)
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email,db)
    if user is None:
        raise credentials_exception
    return user

#function to decode jwt token
def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        return False
    except JWTError:
        return False
    
#function to get user details from token
# def get_user_from_token(token):
#     payload = decode_token(token)
#     if payload:
#         user = get_user_by_email(payload.get("sub"),db)
#         return user
#     else:
#         return False
    
#get user details from token
@router.post("/userme", response_description="Get user details from token")
async def get_user_me(token: str,db: Session=Depends(get_db)):
    user = decode_token(token)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User with this token not found"
            )





#request password reset
@router.post("/reset-password", response_description="Request Password Reset")
async def reset_request(user_email: PasswordRequest,db: Session=Depends(get_db)): 
    user = get_user_by_email(user_email.email,db)
    if user is not None:
        token = create_access_token({"id": user.id})

        #shorten token to 10 random characters
        #token = secrets.token_hex(4)
        

        reset_link = f"http://localhost:8000/?token={token}"

        await password_reset("Password Reset", user.email, {"title": "Password Reset", "reset_link": reset_link})

        return {"message": "Password reset email sent"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User with this email not found"
            )
    

#reset password with provided token
@router.post("/password/{token}", response_description="Reset Password")
async def reset_password(token: str, password: str,db: Session=Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid token"
                )
        user = get_user_by_id(user_id,db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid token"
                )
        user.hashed_password = Hasher.get_password_hash(password)
        db.commit()
        return {"message": "Password successfully updated"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid token"
            )

# activate user email
@router.post("/activate/{token}", response_description="Activate User")
async def activate_user(token: str,db: Session=Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid token"
                )
        user = get_user_by_id(user_id,db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid token"
                )
        user.is_active = True
        db.commit()
        return {"message": "User successfully activated"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid token"
            )

#get otp by sms
@router.post("/otp", response_description="Get OTP")
async def get_otp(user_phone: str,db: Session=Depends(get_db)):
    user = get_user_by_phone(user_phone,db)
    if user is not None:
        #strip phone number to 10 digits and add 234 to the front
        phone = "234" + user_phone[-10:]
        otp = sms_otp(phone,db)
        #await otp_send("OTP", user.phone, {"title": "OTP", "otp": otp})
        return {"message": "OTP sent"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User with this phone number not found"
            )

#update password with otp
@router.post("/password-reset/{otp}", response_description="Update Password")
async def update_password(otp: str, db: Session=Depends(get_db)):
    #check if the sms otp is valid
    if verify_sms_otp(otp,db=db):
        #get the user id from the otp
        return {"message": "Password successfully updated"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid OTP"
            )

#logout user
@router.post("/logout", response_description="Logout User")
async def logout_user(current_user: User = Depends(get_current_user_from_token),db: Session=Depends(get_db)):
    user = get_user_by_id(current_user.id,db)
    if user is not None:
        user.refresh_token = None
        db.commit()
        return {"message": "User successfully logged out"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
            )
    
#get current user from token depending on oauth2_scheme
