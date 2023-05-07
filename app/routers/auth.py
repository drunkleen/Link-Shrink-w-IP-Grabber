from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.database import Session, get_db
from app import models, utility, oauth2
from app.schemas import userschema
from user_agents import parse

router = APIRouter(tags=["Login"])


@router.post("/login", response_model=userschema.Token)
async def login(request: Request,
                user_credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.mail == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid username or password")

    if not utility.password_verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid username or password")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    user_agent = request.headers.get("User-Agent")
    ua_string = str(user_agent)
    user_agent_obj = parse(ua_string)

    new_ip = models.LoginLog(user_mail=user_credentials.username,
                             user_browser=user_agent_obj.browser.family,
                             user_os=user_agent_obj.os.family,
                             user_device=user_agent_obj.device.family,
                             user_ip=request.client.host)

    db.add(new_ip)
    db.commit()
    db.refresh(new_ip)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/SignUp', status_code=status.HTTP_201_CREATED, response_model=userschema.GetUser)
async def create_user(user: userschema.UserCreate, db: Session = Depends(get_db)):
    # hashing password:
    user.password = utility.hash_password(user.password)
    # create the user
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
