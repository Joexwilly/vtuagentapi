from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str
    


class PasswordRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    newpassword: str
  
