from typing import List
from app.utility import hash_password
from fastapi import status, Depends, APIRouter, HTTPException
from app import models, oauth2
from app.database import Session, get_db
from app.schemas import userschema, urlschema

router = APIRouter(
    prefix="/users",
    tags=["Users Handling"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=userschema.GetUser)
async def create_user(user: userschema.UserCreate, db: Session = Depends(get_db)):
    # hashing password:
    user.password = hash_password(user.password)
    # create the user
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/control/',
            status_code=status.HTTP_200_OK,
            response_model=List[urlschema.URLLogOUT])
async def get_user(db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not logged in"
        )

    response = db.query(
        models.URLLog
    ).join(
        models.URL,
        models.URL.id == models.URLLog.url_id,
        isouter=True
    ).filter(
        models.URL.owner_id == current_user.id
    ).all()

    return response
