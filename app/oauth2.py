from http.client import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .schema import TokenData
from fastapi import Depends, status
#SECRET KEY
#ALGORITHM TO USE
#EXPIRATION TIME

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = 'HELLO'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str, exception):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        email = payload.get("email")

        if not email:
            raise exception
        
        token_data = TokenData(email = email)
    except JWTError:
        raise exception
        
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Cant validate', header={"WWW-Authenticate" : "Bearer"})

    return verify_token(token, credentials_exception)