from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone, date, timedelta


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: timedelta
    data: dict
    


class TokenData(BaseModel):
    id: str
    


class PasswordRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    newpassword: str
  
