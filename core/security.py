#core > security.py

from datetime import datetime,timedelta
from typing import Optional
from jose import JWTError, jwt
import base64

from core.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

#use base4 to create access token
# def create_access_token_6digit(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_b64 = base64.b64encode(to_encode)
#     token = encoded_b64.decode()
#     return token


# import jwt

# payload = {'some': 'payload'}
# secret_key = 'secret'
# algorithm = 'HS256'

# token = jwt.encode(payload, secret_key, algorithm=algorithm)

# print(token)  # b'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzb21lIjogInBheWxvYWQifQ.9mmZ6a1Uf-lRjYo7wU6LgUvq5zjW8AT6GEMRYZ9owmc'

