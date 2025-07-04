from fastapi import FastAPI
from . import models, config
from .database import engine
from .routes import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)
#what hashing algorithm will be used

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials =  True, 
    allow_methods = ["*"], 
    allow_headers = ["*"]
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():

    return {"message": "Hello this is James and welcome to My API generation course"}




