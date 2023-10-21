from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware



# models.Base.metadata.create_all(bind=engine) ###this commands is not needed anymore 

app = FastAPI()

origins = ['https://www.google.com', 'https://www.youtube.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, ##this wil be a list of domains that wil have acss to our API 
    allow_credentials=True,
    allow_methods=["*"], ##we can allow specific requests 
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


###grab the router object fro the post and user file in routers folder 
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)