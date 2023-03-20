from typing import Optional
from pydantic import BaseModel, EmailStr

# reset password
class PasswordReset(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str