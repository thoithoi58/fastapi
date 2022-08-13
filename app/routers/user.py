from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..schema import UserCreate, UserResponse
from ..database import get_db
from .. import utils
from .. import models

router = APIRouter(
    prefix="/users",
    tags=['User']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    #Hash the password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    return user