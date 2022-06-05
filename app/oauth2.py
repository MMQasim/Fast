from jose import JWTError, jwt
import datetime
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "usinw3yHTj19KMKrcnGkxS3cIAxo73Dm4OI0jFPgjU1NNMAe6geLi4zklRk39WdHNlHGxNmryb4eIW6OKWg2pByBUQsglyVOYt9SwAzYvjZ7ciDILq78KERajY3w4A94dI9W57uf9ehsV0GPtHcueT5yRkTBKtdgkD5lHP"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.datetime.now()+datetime.timedelta(minutes=30)

    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_access_token(token:str, creanditial_exception,verification_field):
   
    try:
        payload= jwt.decode(SECRET_KEY,token=token,algorithms=ALGORITHM)
        data:str=payload.get(verification_field)
        if data is None:
            raise creanditial_exception
        return data
    except JWTError:
        creanditial_exception

def get_current_user(token:str=Depends(oauth2_scheme)):

    print("ok")

