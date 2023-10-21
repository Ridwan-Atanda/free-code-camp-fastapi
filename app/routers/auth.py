from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(tags = ['Authentication'])


##this logs in new user and creates an access token 
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), ##this knows if its username or phone no or email
          db: Session = Depends(database.get_db)):

    print(f'we are here..............10')
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    ##if the user email is not in the db 
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f'invalid credentials')
    
    #if the user password doesnt match our hashed password in the db 
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f'invalid credentials')
    
    # Create a token 
    print(f'we are here..............11')
    access_token = oauth2.create_access_token(data = {'user_id': user.id}) ###here we create access token for the curresponding user id in the dataase 
    print(user.id)
    
    return{"access_token": access_token, "token_type": 'bearer'}