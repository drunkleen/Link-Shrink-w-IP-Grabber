from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routers import auth, user, url,redirect

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(url.router)
app.include_router(redirect.router)


@app.get('/')
async def root():
    return {'message': 'Welcome to IP-Grabber API'}
