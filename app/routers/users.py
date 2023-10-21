from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix= '/users',
    tags= ['Users']
)

##this create a new user
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Userout)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):  #Post uses the class above to define the type of data we want from the front end 
    
    ####hash the password 

    hashed_password = utils.hash(user.password) ##hash the password 
    user.password = hashed_password  #update users password here to the hashed one 

    new_user = models.User(**user.model_dump()) #this line uses dict form of post instead of the above 

    try:

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        db.rollback()  # Rollback the transaction to avoid leaving the database in an inconsistent state
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    return new_user



####this gets a new user

@router.get("/{id}", response_model= schemas.UserCreate)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"user with {id} not found")
    
    return user

