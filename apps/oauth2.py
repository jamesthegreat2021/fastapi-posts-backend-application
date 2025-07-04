from jose import JWSError, jwt
from datetime import datetime,timedelta
from . import schemas,database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = "P@u9#fX!k3VrQmZ7&tN4Gw%yXcLp$1DhKeRb8HsVo2^TaMzEnLd6JcUy#BmWxYqS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(data: dict):
    to_encode = data.copy()

    expire =  datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception): 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None: 
            raise credentials_exception
        
        token_data = schemas.TokenData(id=str(id))

    except JWSError: 
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)): 
    credentials_exceptions = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"could not validate credentials", headers={"WWW-authenticate": "Bearer"})
   
    token = verify_access_token(token, credentials_exceptions)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    print(user)

    return user
    
