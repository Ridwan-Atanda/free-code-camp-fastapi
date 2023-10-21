from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from .database import get_db
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings



oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login') ##login here is the path 
##Secret_key 

##Algorithm 

##expiration time 


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



##this function generates access token 
def create_access_token(data: dict):

    to_encode = data.copy() #here we copy the unique user id 
    print(f'to_encode........{to_encode}......7')
    print(f'ACCESS_TOKEN_EXPIRE_MINUTES...........{ACCESS_TOKEN_EXPIRE_MINUTES}...8')
    print(type(ACCESS_TOKEN_EXPIRE_MINUTES))

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) ## we create an expiry 

    to_encode.update({'exp': expire}) ##we add the exp to the dict 
    print(f'we are here..............8')


    encodded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM) #we encode user id and expiry
    print(f'encodded_jwt........{encodded_jwt}')
    return encodded_jwt


###this function decodes the accss token and verify if it matches what we saved locally 
def verify_access_token(token: str, credentials_exception): ##this accept the token and also an exception if the token doesnt match 

    print(f'we are here..............2')
    try:
        print(f'token {token}')
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM]) #we decode the token using the parameters set above 

        id : str = str(payload.get("user_id")) ###we get bthe user id from the bearer token and convert to string
        print(f'this is the id we got from frontend {id}')
        print(f'this is the id we got from frontend {type(id)}')
        if id is None:
            raise credentials_exception
        print(f'we are here..............3')
        token_data = schemas.TokenData(id = id)  ##just making sure its string and this is just an id value str
        print(f'token data {token_data}')
        print(f'we are here..............4')
    except JWTError:
        raise credentials_exception
    print(f'we are here..............5')
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f'could not validate credentials', 
                                          headers = {"WWW-Authenticate": 'Bearer'})
    print(f'we are here..............6')


    token = verify_access_token(token, credentials_exception) ##verify the token and extract the id part of the token 
    user = db.query(models.User).filter(models.User.id == token.id).first() #check the d for where the token id (token was created with id and) matches the id in the db 
    
    return user