from email.policy import HTTP
from jose import JWTError, jwt
import datetime
from DB import models
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session
from DB.SqlAlchemy import get_db
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_access_token(token:str, creanditial_exception,verification_field):
   
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        data:str = payload.get(verification_field)
        if data is None:
            raise creanditial_exception
        return data
    except JWTError:
        creanditial_exception

def get_current_user(token:str=Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalide access", headers={"WWW-Authenticate":"Bearer"})
    tokenData=verify_access_token(token,credentials_exception,"id")
    user=db.query(models.User).filter(models.User.id==tokenData).first()
    if not user:
        raise credentials_exception
    return user

