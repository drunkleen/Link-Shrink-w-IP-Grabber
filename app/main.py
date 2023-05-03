from fastapi import FastAPI, Request
from app import models
from app.database import engine
from app.routers import auth, user, url,redirect
from user_agents import parse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(url.router)
app.include_router(redirect.router)


@app.get('/')
async def root():
    return {'message': 'Welcome to IP-Grabber API'}
