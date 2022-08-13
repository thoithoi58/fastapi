from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import oauth2
from ..database import get_db
from ..schema import UserLogin
from .. import models, utils, oauth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
def login(user_info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_info.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not found')

    if not utils.verify(user_info.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong pass')

    access_token = oauth2.create_access_token(data= {"email" : user_info.username})

    return {'access_token': access_token, "token_type": "bearer"}
