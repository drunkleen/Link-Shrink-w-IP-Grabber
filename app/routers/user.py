from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from app import models
from app.database import Session, get_db
from app.utility import hash_password
from app.schemas import userschema

router = APIRouter(
    prefix="/users",
    tags=["Users Handling"]
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[userschema.GetUser])
async def get_all_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()

    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=userschema.GetUser)
async def create_user(user: userschema.UserCreate, db: Session = Depends(get_db)):
    # hashing password:
    print(f"\n\n\n\n{db}\n\n\n\n")
    user.password = hash_password(user.password)
    # create the user
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=userschema.GetUser)
async def get_user(user_id: int, datab: Session = Depends(get_db)):
    user = datab.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"post with {user_id} doesn't exist.")

    return user
